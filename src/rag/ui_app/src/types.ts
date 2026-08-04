import type { ThreadMessage } from "@assistant-ui/react";

export type GatewayStatus = "checking" | "ok" | "warn" | "error";

export type RagSource = {
  id?: string;
  source?: string;
  title?: string;
  source_title?: string;
  url?: string;
  canonical_url?: string;
  chunk_id?: string;
  score?: number | string;
  source_group?: string;
  trust_tier?: string;
  source_type?: string;
  snippet?: string;
  [key: string]: unknown;
};

export type RagAttachment = {
  name: string;
  mime_type: string;
  text: string;
  chars: number;
  kind?: string;
  truncated?: boolean;
};

export type RagRunDetails = {
  requestId: string;
  sources: RagSource[];
  metadata: Record<string, unknown>;
  model: string;
};

export type GatewayInfo = {
  status: GatewayStatus;
  model: string;
  backingModel: string;
  provider: string;
  providerStatus: string;
  baseUrl: string;
  vectorStore: string;
  attachmentsEnabled: boolean;
  attachmentPolicy: string;
};

export type ChatChunk = {
  choices?: Array<{
    delta?: {
      role?: string;
      content?: string;
    };
    finish_reason?: string | null;
  }>;
  model?: string;
  rag_request_id?: string;
  rag_sources?: RagSource[];
  rag_metadata?: Record<string, unknown>;
  error?: {
    message?: string;
  };
};

export type OpenAIMessage = {
  role: ThreadMessage["role"];
  content: string;
};
