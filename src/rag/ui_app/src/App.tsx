import {
  AssistantRuntimeProvider,
  ComposerPrimitive,
  MessagePrimitive,
  ThreadPrimitive,
  ThreadListPrimitive,
  useLocalRuntime,
  type ChatModelAdapter,
  type ThreadMessage,
} from "@assistant-ui/react";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import {
  extractAttachment,
  gatewayUnavailable,
  loadGatewayInfo,
  sourceHref,
  sourceTitle,
  streamChatCompletion,
} from "./gateway";
import type { GatewayInfo, RagAttachment, RagRunDetails, RagSource } from "./types";

const maxAttachmentCount = 3;
const maxAttachmentBytes = 5 * 1024 * 1024;
const sampleAttachmentName = "sample-attachment.md";
const sampleAttachmentText = [
  "# Synthetic attachment acceptance note",
  "",
  "The approval marker is OARC-RAG-ATTACHMENT-READY.",
  "This generated note is safe to send through a private RunPod tunnel.",
].join("\n");
const defaultRunDetails: RagRunDetails = {
  requestId: "None",
  sources: [],
  metadata: {},
  model: "oarc-rag-v1",
};

export function App() {
  const [gateway, setGateway] = useState<GatewayInfo>(gatewayUnavailable());
  const [runDetails, setRunDetails] = useState<RagRunDetails>(defaultRunDetails);
  const [attachments, setAttachments] = useState<RagAttachment[]>([]);
  const [attachmentBusy, setAttachmentBusy] = useState(false);
  const [attachmentError, setAttachmentError] = useState("");
  const attachmentsRef = useRef<RagAttachment[]>([]);

  const syncAttachments = useCallback((nextAttachments: RagAttachment[]) => {
    attachmentsRef.current = nextAttachments;
    setAttachments(nextAttachments);
  }, []);

  useEffect(() => {
    let ignore = false;

    async function refresh() {
      try {
        const info = await loadGatewayInfo();
        if (!ignore) {
          setGateway(info);
        }
      } catch {
        if (!ignore) {
          setGateway(gatewayUnavailable());
        }
      }
    }

    refresh();
    const timer = window.setInterval(refresh, 30_000);
    return () => {
      ignore = true;
      window.clearInterval(timer);
    };
  }, []);

  const handleRunDetails = useCallback((details: RagRunDetails) => {
    setRunDetails(details);
  }, []);

  const processFiles = useCallback(
    async (files: File[]) => {
      if (files.length === 0) {
        return;
      }
      if (!gateway.attachmentsEnabled) {
        setAttachmentError("Attachments are disabled on this deployment.");
        return;
      }

      setAttachmentBusy(true);
      setAttachmentError("");
      try {
        const next = [...attachmentsRef.current];
        for (const file of files) {
          if (next.length >= maxAttachmentCount) {
            throw new Error(`Attach up to ${maxAttachmentCount} files per message.`);
          }
          if (file.size > maxAttachmentBytes) {
            throw new Error(`${file.name} is larger than ${formatBytes(maxAttachmentBytes)}.`);
          }
          next.push(await extractAttachment(file));
          syncAttachments(next);
        }
      } catch (error) {
        setAttachmentError(error instanceof Error ? error.message : "Could not read attachment.");
      } finally {
        setAttachmentBusy(false);
      }
    },
    [gateway.attachmentsEnabled, syncAttachments],
  );

  const runtime = useOarcRuntime({
    model: gateway.model,
    attachmentsRef,
    onAttachmentsConsumed: () => syncAttachments([]),
    onRunDetails: handleRunDetails,
  });

  const addFiles = useCallback(
    async (files: FileList | null) => {
      await processFiles(Array.from(files || []));
    },
    [processFiles],
  );

  const addSampleAttachment = useCallback(
    async () => {
      await processFiles([
        new File([sampleAttachmentText], sampleAttachmentName, { type: "text/markdown" }),
      ]);
    },
    [processFiles],
  );

  const removeAttachment = useCallback(
    (index: number) => {
      syncAttachments(attachmentsRef.current.filter((_, itemIndex) => itemIndex !== index));
    },
    [syncAttachments],
  );

  const clearRunDetails = useCallback(() => {
    setRunDetails(defaultRunDetails);
    setAttachmentError("");
    syncAttachments([]);
  }, [syncAttachments]);

  return (
    <AssistantRuntimeProvider runtime={runtime}>
      <div className="app-shell">
        <Rail gateway={gateway} onClear={clearRunDetails} />
        <div className="main-stack">
          <Header gateway={gateway} />
          <main className="workspace">
            <section className="thread-pane" aria-label="Chat conversation">
              <ChatThread
                attachments={attachments}
                attachmentBusy={attachmentBusy}
                attachmentError={attachmentError}
                attachmentsEnabled={gateway.attachmentsEnabled}
                attachmentPolicy={gateway.attachmentPolicy}
                onAddFiles={addFiles}
                onAddSampleAttachment={addSampleAttachment}
                onRemoveAttachment={removeAttachment}
                onClear={clearRunDetails}
              />
            </section>
            <SourceInspector details={runDetails} gateway={gateway} />
          </main>
        </div>
      </div>
    </AssistantRuntimeProvider>
  );
}

function useOarcRuntime({
  model,
  attachmentsRef,
  onAttachmentsConsumed,
  onRunDetails,
}: {
  model: string;
  attachmentsRef: React.MutableRefObject<RagAttachment[]>;
  onAttachmentsConsumed: () => void;
  onRunDetails: (details: RagRunDetails) => void;
}) {
  const adapter = useMemo<ChatModelAdapter>(
    () => ({
      run: async function* ({ messages, abortSignal }) {
        const requestAttachments = attachmentsRef.current;
        onAttachmentsConsumed();

        let text = "";
        let finalDetails: RagRunDetails | undefined;
        const openAiMessages = messages.map(toOpenAIMessage).filter((message) => message.content);

        for await (const update of streamChatCompletion({
          model,
          messages: openAiMessages,
          attachments: requestAttachments,
          abortSignal,
        })) {
          text = update.text;
          if (update.details) {
            finalDetails = update.details;
            onRunDetails(update.details);
          }
          yield {
            content: text ? [{ type: "text", text }] : [],
            metadata: finalDetails
              ? {
                  custom: {
                    rag_request_id: finalDetails.requestId,
                    rag_sources: finalDetails.sources,
                    rag_metadata: finalDetails.metadata,
                  },
                }
              : undefined,
          };
        }

        if (!text.trim()) {
          text = "No answer content returned.";
        }

        yield {
          content: [{ type: "text", text }],
          metadata: finalDetails
            ? {
                custom: {
                  rag_request_id: finalDetails.requestId,
                  rag_sources: finalDetails.sources,
                  rag_metadata: finalDetails.metadata,
                },
              }
            : undefined,
        };
      },
    }),
    [attachmentsRef, model, onAttachmentsConsumed, onRunDetails],
  );

  return useLocalRuntime(adapter);
}

function Rail({ gateway, onClear }: { gateway: GatewayInfo; onClear: () => void }) {
  return (
    <aside className="chat-rail" aria-label="Chat sessions">
      <div className="rail-brand">
        <span className="brand-mark" aria-hidden="true">OA</span>
        <div>
          <strong>OARC RAG</strong>
          <span>assistant-ui thread</span>
        </div>
      </div>
      <ThreadListPrimitive.New className="rail-new" type="button" onClick={onClear}>
        New chat
      </ThreadListPrimitive.New>
      <div className="rail-group" aria-label="Runtime">
        <span>Endpoint</span>
        <strong>/v1/chat/completions</strong>
      </div>
      <div className="rail-group" aria-label="Attachment status">
        <span>Attachments</span>
        <strong>{gateway.attachmentsEnabled ? "Enabled for test" : "Disabled"}</strong>
      </div>
    </aside>
  );
}

function Header({ gateway }: { gateway: GatewayInfo }) {
  return (
    <header className="topbar" aria-label="Gateway status">
      <div className="brand-block">
        <span className="template-label">assistant-ui template</span>
        <h1>OARC Chat Assistant</h1>
        <p>
          {gateway.model} · {gateway.backingModel}
        </p>
      </div>
      <div className="status-row" aria-live="polite">
        <StatusPill status={gateway.status}>
          {gateway.status === "ok" ? "Provider ok" : `Provider ${gateway.providerStatus}`}
        </StatusPill>
        <StatusPill status="warn">{gateway.vectorStore}</StatusPill>
      </div>
    </header>
  );
}

function ChatThread({
  attachments,
  attachmentBusy,
  attachmentError,
  attachmentsEnabled,
  attachmentPolicy,
  onAddFiles,
  onAddSampleAttachment,
  onRemoveAttachment,
  onClear,
}: {
  attachments: RagAttachment[];
  attachmentBusy: boolean;
  attachmentError: string;
  attachmentsEnabled: boolean;
  attachmentPolicy: string;
  onAddFiles: (files: FileList | null) => void;
  onAddSampleAttachment: () => void;
  onRemoveAttachment: (index: number) => void;
  onClear: () => void;
}) {
  return (
    <ThreadPrimitive.Root className="thread-root">
      <ThreadPrimitive.Viewport className="thread-viewport">
        <ThreadPrimitive.Empty>
          <div className="empty-chat">What can I help with?</div>
        </ThreadPrimitive.Empty>
        <ThreadPrimitive.Messages>
          {({ message }) => <ChatMessage message={message} />}
        </ThreadPrimitive.Messages>
        <ThreadPrimitive.ViewportFooter className="thread-footer">
          <Composer
            attachments={attachments}
            attachmentBusy={attachmentBusy}
            attachmentError={attachmentError}
            attachmentsEnabled={attachmentsEnabled}
            attachmentPolicy={attachmentPolicy}
            onAddFiles={onAddFiles}
            onAddSampleAttachment={onAddSampleAttachment}
            onRemoveAttachment={onRemoveAttachment}
            onClear={onClear}
          />
        </ThreadPrimitive.ViewportFooter>
      </ThreadPrimitive.Viewport>
    </ThreadPrimitive.Root>
  );
}

function ChatMessage({ message }: { message: ThreadMessage }) {
  const custom = message.metadata.custom as
    | {
        rag_request_id?: string;
        rag_sources?: RagSource[];
      }
    | undefined;
  const sources = custom?.rag_sources || [];

  return (
    <MessagePrimitive.Root className={`message message-${message.role}`}>
      <div className="avatar" aria-hidden="true">
        {message.role === "user" ? "You" : "AI"}
      </div>
      <div className="message-body">
        <div className="message-content">
          {message.content.map((part, index) => {
            if (part.type === "text") {
              return <TextPart key={index} text={part.text} />;
            }
            if (part.type === "source") {
              return <span key={index} className="inline-source">{part.title}</span>;
            }
            return null;
          })}
          {message.role === "assistant" && message.status?.type === "running" ? (
            <span className="stream-caret" aria-label="Answer streaming" />
          ) : null}
        </div>
        {custom?.rag_request_id ? (
          <div className="message-foot">
            <span>{custom.rag_request_id}</span>
            <span>{sources.length} source{sources.length === 1 ? "" : "s"}</span>
          </div>
        ) : null}
      </div>
    </MessagePrimitive.Root>
  );
}

function TextPart({ text }: { text: string }) {
  const blocks = splitMarkdownBlocks(text);
  return (
    <>
      {blocks.map((block, index) =>
        block.kind === "code" ? (
          <pre key={index} data-language={block.language || undefined}>
            <code>{block.content}</code>
          </pre>
        ) : (
          <p key={index}>{renderInlineCode(block.content)}</p>
        ),
      )}
    </>
  );
}

function Composer({
  attachments,
  attachmentBusy,
  attachmentError,
  attachmentsEnabled,
  attachmentPolicy,
  onAddFiles,
  onAddSampleAttachment,
  onRemoveAttachment,
  onClear,
}: {
  attachments: RagAttachment[];
  attachmentBusy: boolean;
  attachmentError: string;
  attachmentsEnabled: boolean;
  attachmentPolicy: string;
  onAddFiles: (files: FileList | null) => void;
  onAddSampleAttachment: () => void;
  onRemoveAttachment: (index: number) => void;
  onClear: () => void;
}) {
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  return (
    <ComposerPrimitive.Root className="composer" compact>
      <AttachmentTray
        attachments={attachments}
        busy={attachmentBusy}
        error={attachmentError}
        onRemoveAttachment={onRemoveAttachment}
      />
      <div className={`attachment-policy ${attachmentsEnabled ? "" : "warn"}`}>
        {attachmentsEnabled
          ? attachmentPolicy ||
            "Attachments are sent to this gateway for one request only. Use non-sensitive files."
          : "Attachments are disabled on this deployment. Relaunch with --enable-ui-attachments for private tunnel testing."}
      </div>
      <div className="attachment-testbar">
        <button
          className="sample-attachment-button"
          type="button"
          disabled={!attachmentsEnabled || attachmentBusy}
          title={
            attachmentsEnabled
              ? "Attach a generated Markdown test note"
              : "Enable UI attachments before testing the sample note"
          }
          onClick={onAddSampleAttachment}
        >
          Sample
        </button>
        <span>
          {attachmentsEnabled
            ? "Generated Markdown note tests extraction and rag_attachments without private files."
            : "Sample attachment test is locked until the gateway advertises attachments."}
        </span>
      </div>
      <div className="composer-box">
        <ComposerPrimitive.Input
          className="composer-input"
          placeholder="Message OARC Chat Assistant"
          rows={1}
          submitMode="enter"
        />
        <div className="composer-actions">
          <input
            ref={fileInputRef}
            type="file"
            accept=".txt,.md,.markdown,.pdf,text/plain,text/markdown,application/pdf"
            multiple
            hidden
            onChange={(event) => {
              onAddFiles(event.currentTarget.files);
              event.currentTarget.value = "";
            }}
          />
          <button
            className="control-button"
            type="button"
            disabled={!attachmentsEnabled || attachmentBusy}
            title={
              attachmentsEnabled
                ? "Attach a file"
                : "Attachments disabled on this deployment"
            }
            onClick={() => fileInputRef.current?.click()}
          >
            Attach
          </button>
          <ComposerPrimitive.Cancel className="control-button" title="Stop generation">
            Stop
          </ComposerPrimitive.Cancel>
          <ClearButton onClear={onClear} />
          <ComposerPrimitive.Send className="send-button" title="Send message">
            Send
          </ComposerPrimitive.Send>
        </div>
      </div>
    </ComposerPrimitive.Root>
  );
}

function ClearButton({ onClear }: { onClear: () => void }) {
  return (
    <ThreadListPrimitive.New
      className="control-button"
      type="button"
      title="Clear chat"
      onClick={onClear}
    >
      Clear
    </ThreadListPrimitive.New>
  );
}

function AttachmentTray({
  attachments,
  busy,
  error,
  onRemoveAttachment,
}: {
  attachments: RagAttachment[];
  busy: boolean;
  error: string;
  onRemoveAttachment: (index: number) => void;
}) {
  if (attachments.length === 0 && !busy && !error) {
    return null;
  }

  return (
    <div className="attachment-tray" aria-live="polite">
      {attachments.map((attachment, index) => (
        <span className="attachment-chip" key={`${attachment.name}-${index}`}>
          <span>{attachment.name}</span>
          <small>{attachment.chars.toLocaleString()} chars</small>
          <button
            type="button"
            title={`Remove ${attachment.name}`}
            onClick={() => onRemoveAttachment(index)}
          >
            x
          </button>
        </span>
      ))}
      {busy ? <span className="attachment-chip">Reading file...</span> : null}
      {error ? <span className="attachment-error">{error}</span> : null}
    </div>
  );
}

function SourceInspector({
  details,
  gateway,
}: {
  details: RagRunDetails;
  gateway: GatewayInfo;
}) {
  return (
    <aside className="inspector" aria-label="Sources and metadata">
      <div className="inspector-section">
        <div className="section-title">
          <h2>Sources</h2>
          <span>{details.requestId}</span>
        </div>
        <SourceList sources={details.sources} />
      </div>
      <div className="inspector-section">
        <h2>Run</h2>
        <dl className="detail-list">
          <div>
            <dt>Provider</dt>
            <dd>
              {gateway.provider} · {gateway.providerStatus}
            </dd>
          </div>
          <div>
            <dt>Model</dt>
            <dd>{details.model || gateway.model}</dd>
          </div>
          <div>
            <dt>Base URL</dt>
            <dd>{gateway.baseUrl}</dd>
          </div>
          <div>
            <dt>Vector store</dt>
            <dd>{gateway.vectorStore}</dd>
          </div>
        </dl>
        <pre className="metadata">{JSON.stringify(details.metadata || {}, null, 2)}</pre>
      </div>
    </aside>
  );
}

function SourceList({ sources }: { sources: RagSource[] }) {
  if (!sources.length) {
    return <p className="empty-state">No sources yet.</p>;
  }

  return (
    <div className="source-list">
      {sources.map((source, index) => {
        const href = sourceHref(source);
        return (
          <article className="source-card" key={`${source.chunk_id || source.id || index}`}>
            <h3>
              {href ? (
                <a href={href} target="_blank" rel="noreferrer">
                  {sourceTitle(source, index)}
                </a>
              ) : (
                sourceTitle(source, index)
              )}
            </h3>
            <div className="source-meta">
              <MetaChip label="chunk" value={source.chunk_id} />
              <MetaChip label="score" value={source.score} />
              <MetaChip label="group" value={source.source_group} />
              <MetaChip label="tier" value={source.trust_tier} />
            </div>
            {source.snippet ? <p>{source.snippet}</p> : null}
          </article>
        );
      })}
    </div>
  );
}

function MetaChip({ label, value }: { label: string; value: unknown }) {
  if (value === undefined || value === null || value === "") {
    return null;
  }
  return (
    <span className="meta-chip">
      {label}: {String(value)}
    </span>
  );
}

function StatusPill({
  status,
  children,
}: {
  status: GatewayInfo["status"];
  children: React.ReactNode;
}) {
  return <span className={`status-pill status-${status}`}>{children}</span>;
}

function toOpenAIMessage(message: ThreadMessage) {
  return {
    role: message.role,
    content: message.content
      .map((part) => {
        if (part.type === "text") {
          return part.text;
        }
        if (part.type === "file") {
          return `[file: ${part.filename || "attachment"}]`;
        }
        return "";
      })
      .filter(Boolean)
      .join("\n\n"),
  };
}

function splitMarkdownBlocks(text: string): Array<
  | {
      kind: "paragraph";
      content: string;
    }
  | {
      kind: "code";
      content: string;
      language: string;
    }
> {
  const blocks: Array<
    | {
        kind: "paragraph";
        content: string;
      }
    | {
        kind: "code";
        content: string;
        language: string;
      }
  > = [];
  const fencePattern = /```([a-zA-Z0-9_-]+)?\n?([\s\S]*?)```/g;
  let offset = 0;
  let match = fencePattern.exec(text);

  while (match) {
    blocks.push(...paragraphBlocks(text.slice(offset, match.index)));
    blocks.push({
      kind: "code",
      language: match[1] || "",
      content: match[2].trimEnd(),
    });
    offset = fencePattern.lastIndex;
    match = fencePattern.exec(text);
  }

  blocks.push(...paragraphBlocks(text.slice(offset)));
  return blocks;
}

function paragraphBlocks(text: string) {
  return text
    .split(/\n{2,}/)
    .map((part) => part.trim())
    .filter(Boolean)
    .map((content) => ({ kind: "paragraph" as const, content }));
}

function renderInlineCode(text: string) {
  const parts = text.split(/(`[^`]+`)/g).filter(Boolean);
  return parts.map((part, index) => {
    if (part.startsWith("`") && part.endsWith("`")) {
      return <code key={index}>{part.slice(1, -1)}</code>;
    }
    return part.split("\n").map((line, lineIndex) => (
      <span key={`${index}-${lineIndex}`}>
        {lineIndex > 0 ? <br /> : null}
        {line}
      </span>
    ));
  });
}

function formatBytes(bytes: number) {
  if (bytes < 1024) {
    return `${bytes} B`;
  }
  if (bytes < 1024 * 1024) {
    return `${Math.round(bytes / 102.4) / 10} KB`;
  }
  return `${Math.round(bytes / 1024 / 102.4) / 10} MB`;
}
