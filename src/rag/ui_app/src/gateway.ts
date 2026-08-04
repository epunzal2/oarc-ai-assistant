import type {
  ChatChunk,
  GatewayInfo,
  OpenAIMessage,
  RagAttachment,
  RagRunDetails,
  RagSource,
} from "./types";

const defaultGatewayInfo: GatewayInfo = {
  status: "checking",
  model: "oarc-rag-v1",
  backingModel: "backing model unknown",
  provider: "unknown",
  providerStatus: "unknown",
  baseUrl: "unknown",
  vectorStore: "vector store",
  attachmentsEnabled: false,
  attachmentPolicy: "",
};

type SseMessage =
  | { done: true }
  | {
      done?: false;
      event: string;
      payload: ChatChunk;
    };

export async function loadGatewayInfo(): Promise<GatewayInfo> {
  const [healthResponse, modelsResponse] = await Promise.all([
    fetch("/health", { headers: { Accept: "application/json" } }),
    fetch("/v1/models", { headers: { Accept: "application/json" } }),
  ]);

  if (!healthResponse.ok || !modelsResponse.ok) {
    throw new Error("Gateway status request failed.");
  }

  const health = await healthResponse.json();
  const models = await modelsResponse.json();
  const backend = health.backend || {};
  const providerHealth = backend.provider_health || {};
  const ui = health.ui || {};
  const model = models.data?.[0]?.id || health.model || defaultGatewayInfo.model;
  const providerStatus = providerHealth.status || "unknown";

  return {
    status: providerStatus === "ok" ? "ok" : "warn",
    model,
    backingModel: backend.backing_model || "backing model unknown",
    provider: backend.backing_provider || "unknown",
    providerStatus,
    baseUrl: backend.backing_base_url || "unknown",
    vectorStore: backend.vector_store_type || "vector store",
    attachmentsEnabled: Boolean(ui.attachments_enabled),
    attachmentPolicy: ui.attachment_policy || "",
  };
}

export function gatewayUnavailable(): GatewayInfo {
  return {
    ...defaultGatewayInfo,
    status: "error",
  };
}

export async function extractAttachment(file: File): Promise<RagAttachment> {
  const response = await fetch("/ui/attachments/extract", {
    method: "POST",
    headers: {
      "Content-Type": file.type || "application/octet-stream",
      "X-Attachment-Name": encodeURIComponent(file.name),
    },
    body: file,
  });

  if (!response.ok) {
    let message = `Could not read ${file.name}.`;
    try {
      const payload = await response.json();
      message = payload.error?.message || message;
    } catch {
      message = (await response.text()) || message;
    }
    throw new Error(message);
  }

  return response.json();
}

export async function* streamChatCompletion({
  model,
  messages,
  attachments,
  abortSignal,
}: {
  model: string;
  messages: OpenAIMessage[];
  attachments: RagAttachment[];
  abortSignal: AbortSignal;
}): AsyncGenerator<{ text: string; details?: RagRunDetails }, void> {
  const response = await fetch("/v1/chat/completions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "text/event-stream",
    },
    body: JSON.stringify({
      model,
      stream: true,
      messages,
      rag_attachments: attachments.map((attachment) => ({
        name: attachment.name,
        mime_type: attachment.mime_type,
        text: attachment.text,
      })),
    }),
    signal: abortSignal,
  });

  if (!response.ok) {
    throw new Error(await responseErrorMessage(response));
  }
  if (!response.body) {
    throw new Error("Streaming response body is unavailable.");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  let text = "";
  let details: RagRunDetails | undefined;

  while (true) {
    const { value, done } = await reader.read();
    if (done) {
      break;
    }

    buffer += decoder.decode(value, { stream: true });
    const blocks = buffer.split(/\n\n/);
    buffer = blocks.pop() || "";

    for (const block of blocks) {
      const message = parseSseBlock(block);
      if (!message) {
        continue;
      }
      if (message.done) {
        return;
      }
      if (message.event === "error") {
        throw new Error(message.payload.error?.message || "Gateway streaming error.");
      }

      const delta = message.payload.choices?.[0]?.delta || {};
      if (delta.content) {
        text += delta.content;
        yield { text };
      }

      if (message.payload.rag_request_id) {
        details = {
          requestId: message.payload.rag_request_id,
          sources: message.payload.rag_sources || [],
          metadata: message.payload.rag_metadata || {},
          model: message.payload.model || model,
        };
        yield { text, details };
      }
    }
  }

  if (buffer.trim()) {
    const message = parseSseBlock(buffer);
    if (message && !message.done && message.payload.rag_request_id) {
      details = {
        requestId: message.payload.rag_request_id,
        sources: message.payload.rag_sources || [],
        metadata: message.payload.rag_metadata || {},
        model: message.payload.model || model,
      };
      yield { text, details };
    }
  }
}

export function sourceTitle(source: RagSource, index: number): string {
  return (
    source.title ||
    source.source_title ||
    source.source ||
    source.url ||
    source.canonical_url ||
    source.chunk_id ||
    `Source ${index + 1}`
  ).toString();
}

export function sourceHref(source: RagSource): string | undefined {
  const href = source.url || source.canonical_url;
  return typeof href === "string" && href ? href : undefined;
}

function parseSseBlock(block: string): SseMessage | null {
  let event = "message";
  const data: string[] = [];

  for (const line of block.split(/\r?\n/)) {
    if (!line || line.startsWith(":")) {
      continue;
    }
    if (line.startsWith("event:")) {
      event = line.slice(6).trim();
      continue;
    }
    if (line.startsWith("data:")) {
      data.push(line.slice(5).trimStart());
    }
  }

  const payload = data.join("\n");
  if (!payload) {
    return null;
  }
  if (payload === "[DONE]") {
    return { done: true };
  }
  return { event, payload: JSON.parse(payload) };
}

async function responseErrorMessage(response: Response): Promise<string> {
  let message = `Gateway returned ${response.status}.`;
  try {
    const payload = await response.json();
    message = payload.error?.message || message;
  } catch {
    const text = await response.text();
    message = text || message;
  }
  return message;
}
