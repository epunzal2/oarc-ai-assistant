const modelLine = document.querySelector("#model-line");
const healthPill = document.querySelector("#health-pill");
const vectorPill = document.querySelector("#vector-pill");
const providerLine = document.querySelector("#provider-line");
const baseUrlLine = document.querySelector("#base-url-line");
const requestIdLine = document.querySelector("#request-id");
const sourcesEl = document.querySelector("#sources");
const metadataEl = document.querySelector("#metadata");
const detailsTray = document.querySelector(".details-tray");
const conversationEl = document.querySelector("#conversation");
const form = document.querySelector("#chat-form");
const input = document.querySelector("#question-input");
const sendButton = document.querySelector("#send-button");
const stopButton = document.querySelector("#stop-button");
const clearButton = document.querySelector("#clear-button");
const themeButton = document.querySelector("#theme-button");
const attachButton = document.querySelector("#attach-button");
const fileInput = document.querySelector("#file-input");
const attachmentList = document.querySelector("#attachment-list");
const attachmentPolicy = document.querySelector("#attachment-policy");
const themeStorageKey = "oarc-rag-theme";
const maxAttachmentCount = 3;
const maxAttachmentBytes = 5 * 1024 * 1024;

const state = {
  activeController: null,
  activeAssistant: null,
  model: "oarc-rag-v1",
  theme: "light",
  attachments: [],
  attachmentError: "",
  attachmentBusy: false,
  attachmentsEnabled: false,
  attachmentPolicy: "",
};

function storedTheme() {
  try {
    const theme = window.localStorage.getItem(themeStorageKey);
    return theme === "dark" || theme === "light" ? theme : null;
  } catch {
    return null;
  }
}

function systemTheme() {
  return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
}

function saveTheme(theme) {
  try {
    window.localStorage.setItem(themeStorageKey, theme);
  } catch {
    // Theme persistence is optional; the UI still works if storage is disabled.
  }
}

function applyTheme(theme, { persist = false } = {}) {
  state.theme = theme;
  document.documentElement.dataset.theme = theme;
  themeButton.textContent = theme === "dark" ? "Light" : "Dark";
  themeButton.title = theme === "dark" ? "Switch to light mode" : "Switch to dark mode";
  themeButton.setAttribute("aria-pressed", String(theme === "dark"));
  if (persist) {
    saveTheme(theme);
  }
}

function setPill(el, text, statusClass) {
  el.textContent = text;
  el.className = `status-pill ${statusClass || ""}`.trim();
}

function renderEmptyChat() {
  conversationEl.innerHTML = "";
  const empty = document.createElement("div");
  empty.className = "empty-chat";
  empty.textContent = "What can I help with?";
  conversationEl.append(empty);
}

function ensureConversationReady() {
  const empty = conversationEl.querySelector(".empty-chat");
  if (empty) {
    empty.remove();
  }
}

function appendMessage(role, content, className = role) {
  ensureConversationReady();
  const article = document.createElement("article");
  article.className = `message ${className}`;

  const roleEl = document.createElement("div");
  roleEl.className = "message-role";
  roleEl.textContent = role;

  const contentEl = document.createElement("div");
  contentEl.className = "message-content";
  if (className === "assistant") {
    renderAssistantContent(contentEl, content);
  } else {
    contentEl.textContent = content;
  }

  const footEl = document.createElement("div");
  footEl.className = "message-foot";
  footEl.hidden = true;

  article.append(roleEl, contentEl, footEl);
  conversationEl.append(article);
  conversationEl.scrollTop = conversationEl.scrollHeight;
  return { article, contentEl, footEl, rawText: content };
}

function setBusy(isBusy) {
  sendButton.disabled = isBusy || state.attachmentBusy;
  stopButton.disabled = !isBusy;
  input.disabled = isBusy;
  attachButton.disabled = isBusy || state.attachmentBusy || !state.attachmentsEnabled;
}

function resizeComposer() {
  input.style.height = "auto";
  input.style.height = `${Math.min(input.scrollHeight, 180)}px`;
}

function updateAssistantFoot(assistant, requestId, sources) {
  if (!assistant || !requestId) {
    return;
  }
  assistant.footEl.hidden = false;
  assistant.footEl.textContent = `${requestId} · ${(sources || []).length} source${
    (sources || []).length === 1 ? "" : "s"
  }`;
}

function attachmentRequestPayload() {
  return state.attachments.map((attachment) => ({
    name: attachment.name,
    mime_type: attachment.mime_type,
    text: attachment.text,
  }));
}

function clearAttachments() {
  state.attachments = [];
  state.attachmentError = "";
  fileInput.value = "";
  renderAttachments();
}

function formatBytes(bytes) {
  if (bytes < 1024) {
    return `${bytes} B`;
  }
  if (bytes < 1024 * 1024) {
    return `${Math.round(bytes / 102.4) / 10} KB`;
  }
  return `${Math.round(bytes / 1024 / 102.4) / 10} MB`;
}

function renderAttachments() {
  attachmentList.replaceChildren();
  if (state.attachments.length === 0 && !state.attachmentError && !state.attachmentBusy) {
    attachmentList.hidden = true;
    return;
  }

  attachmentList.hidden = false;
  for (const [index, attachment] of state.attachments.entries()) {
    const chip = document.createElement("span");
    chip.className = "attachment-chip";

    const name = document.createElement("span");
    name.textContent = attachment.name;
    chip.append(name);

    const size = document.createElement("small");
    size.textContent = `${attachment.chars.toLocaleString()} chars`;
    chip.append(size);

    const remove = document.createElement("button");
    remove.type = "button";
    remove.title = `Remove ${attachment.name}`;
    remove.textContent = "x";
    remove.addEventListener("click", () => {
      state.attachments.splice(index, 1);
      renderAttachments();
    });
    chip.append(remove);
    attachmentList.append(chip);
  }

  if (state.attachmentBusy) {
    const chip = document.createElement("span");
    chip.className = "attachment-chip";
    chip.textContent = "Reading file...";
    attachmentList.append(chip);
  }

  if (state.attachmentError) {
    const error = document.createElement("span");
    error.className = "attachment-error";
    error.textContent = state.attachmentError;
    attachmentList.append(error);
  }
}

function renderAttachmentPolicy() {
  attachmentPolicy.hidden = false;
  attachmentPolicy.classList.toggle("warn", !state.attachmentsEnabled);
  if (state.attachmentsEnabled) {
    attachmentPolicy.textContent =
      state.attachmentPolicy ||
      "Attachments are sent to this gateway for one request only. Use non-sensitive files.";
    attachButton.title = "Attach file";
  } else {
    attachmentPolicy.textContent =
      "Attachments are disabled on this deployment. Enable only for private tunnel testing.";
    attachButton.title = "Attachments disabled on this deployment";
    clearAttachments();
  }
  setBusy(Boolean(state.activeController));
}

async function extractAttachment(file) {
  if (file.size > maxAttachmentBytes) {
    throw new Error(`${file.name} is larger than ${formatBytes(maxAttachmentBytes)}.`);
  }

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

async function addFiles(files) {
  const selected = Array.from(files || []);
  if (selected.length === 0) {
    return;
  }
  if (!state.attachmentsEnabled) {
    state.attachmentError = "Attachments are disabled on this deployment.";
    renderAttachments();
    return;
  }

  state.attachmentError = "";
  state.attachmentBusy = true;
  setBusy(Boolean(state.activeController));
  renderAttachments();

  try {
    for (const file of selected) {
      if (state.attachments.length >= maxAttachmentCount) {
        throw new Error(`Attach up to ${maxAttachmentCount} files per message.`);
      }
      const attachment = await extractAttachment(file);
      state.attachments.push(attachment);
      renderAttachments();
    }
  } catch (error) {
    state.attachmentError = error.message || "Could not read attachment.";
  } finally {
    state.attachmentBusy = false;
    setBusy(Boolean(state.activeController));
    fileInput.value = "";
    renderAttachments();
  }
}

function appendInlineText(parent, text) {
  const pattern = /`([^`]+)`/g;
  let offset = 0;
  let match = pattern.exec(text);
  while (match) {
    if (match.index > offset) {
      parent.append(document.createTextNode(text.slice(offset, match.index)));
    }
    const code = document.createElement("code");
    code.textContent = match[1];
    parent.append(code);
    offset = pattern.lastIndex;
    match = pattern.exec(text);
  }
  if (offset < text.length) {
    parent.append(document.createTextNode(text.slice(offset)));
  }
}

function appendParagraphs(parent, text) {
  const paragraphs = text.split(/\n{2,}/).filter((part) => part.trim());
  for (const paragraphText of paragraphs) {
    const paragraph = document.createElement("p");
    const lines = paragraphText.split("\n");
    lines.forEach((line, index) => {
      if (index > 0) {
        paragraph.append(document.createElement("br"));
      }
      appendInlineText(paragraph, line);
    });
    parent.append(paragraph);
  }
}

function renderAssistantContent(el, text) {
  el.replaceChildren();
  if (!text) {
    return;
  }

  const fencePattern = /```([a-zA-Z0-9_-]+)?\n?([\s\S]*?)```/g;
  let offset = 0;
  let match = fencePattern.exec(text);
  while (match) {
    appendParagraphs(el, text.slice(offset, match.index));
    const pre = document.createElement("pre");
    const code = document.createElement("code");
    if (match[1]) {
      pre.dataset.language = match[1];
    }
    code.textContent = match[2].trimEnd();
    pre.append(code);
    el.append(pre);
    offset = fencePattern.lastIndex;
    match = fencePattern.exec(text);
  }
  appendParagraphs(el, text.slice(offset));
}

function sourceTitle(source, index) {
  return (
    source.title ||
    source.source_title ||
    source.source ||
    source.url ||
    source.canonical_url ||
    source.chunk_id ||
    `Source ${index + 1}`
  );
}

function appendChip(parent, label, value) {
  if (value === undefined || value === null || value === "") {
    return;
  }
  const chip = document.createElement("span");
  chip.className = "source-chip";
  chip.textContent = `${label}: ${value}`;
  parent.append(chip);
}

function renderSources(sources) {
  sourcesEl.innerHTML = "";
  if (!sources) {
    sourcesEl.className = "sources empty-state";
    sourcesEl.textContent = "No sources yet.";
    return;
  }
  if (sources.length === 0) {
    sourcesEl.className = "sources empty-state";
    sourcesEl.textContent = "No sources returned.";
    return;
  }

  sourcesEl.className = "sources";
  sources.forEach((source, index) => {
    const card = document.createElement("article");
    card.className = "source-card";

    const title = document.createElement("h3");
    title.className = "source-title";
    const href = source.url || source.canonical_url;
    if (href) {
      const link = document.createElement("a");
      link.href = href;
      link.target = "_blank";
      link.rel = "noreferrer";
      link.textContent = sourceTitle(source, index);
      title.append(link);
    } else {
      title.textContent = sourceTitle(source, index);
    }

    const meta = document.createElement("div");
    meta.className = "source-meta";
    appendChip(meta, "chunk", source.chunk_id);
    appendChip(meta, "score", source.score);
    appendChip(meta, "group", source.source_group);
    appendChip(meta, "tier", source.trust_tier);

    card.append(title);
    if (meta.children.length > 0) {
      card.append(meta);
    }
    if (source.snippet) {
      const snippet = document.createElement("p");
      snippet.className = "source-snippet";
      snippet.textContent = source.snippet;
      card.append(snippet);
    }
    sourcesEl.append(card);
  });
}

function renderMetadata(metadata) {
  metadataEl.textContent = JSON.stringify(metadata || {}, null, 2);
}

async function refreshStatus() {
  try {
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
    const model = models.data && models.data[0] ? models.data[0].id : health.model || state.model;
    state.model = model || state.model;
    state.attachmentsEnabled = Boolean(ui.attachments_enabled);
    state.attachmentPolicy = ui.attachment_policy || "";
    renderAttachmentPolicy();

    modelLine.textContent = `${state.model} · ${backend.backing_model || "backing model unknown"}`;
    providerLine.textContent = `${backend.backing_provider || "unknown"} · ${
      providerHealth.status || "unknown"
    }`;
    baseUrlLine.textContent = backend.backing_base_url || "Unknown";
    setPill(
      healthPill,
      providerHealth.status === "ok"
        ? "Provider ok"
        : `Provider ${providerHealth.status || "unknown"}`,
      providerHealth.status === "ok" ? "status-ok" : "status-warn",
    );
    setPill(vectorPill, backend.vector_store_type || "Vector store", "status-pending");
  } catch (error) {
    modelLine.textContent = "Gateway unavailable";
    providerLine.textContent = "Unknown";
    baseUrlLine.textContent = "Unknown";
    state.attachmentsEnabled = false;
    state.attachmentPolicy = "";
    renderAttachmentPolicy();
    setPill(healthPill, "Gateway error", "status-error");
    setPill(vectorPill, "Vector store", "status-pending");
  }
}

function parseSseBlock(block) {
  let event = "message";
  const data = [];
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

async function streamAnswer(question, attachments = []) {
  const controller = new AbortController();
  state.activeController = controller;
  setBusy(true);
  detailsTray.hidden = false;
  requestIdLine.textContent = "Pending";
  detailsTray.open = false;
  renderSources(null);
  renderMetadata({});

  const userMessage = appendMessage("user", question);
  if (attachments.length > 0) {
    userMessage.footEl.hidden = false;
    userMessage.footEl.textContent = `Attached: ${attachments
      .map((attachment) => attachment.name)
      .join(", ")}`;
  }
  const assistant = appendMessage("assistant", "");
  state.activeAssistant = assistant;

  try {
    const response = await fetch("/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "text/event-stream",
      },
      body: JSON.stringify({
        model: state.model,
        stream: true,
        messages: [{ role: "user", content: question }],
        rag_attachments: attachments,
      }),
      signal: controller.signal,
    });

    if (!response.ok) {
      let message = `Gateway returned ${response.status}.`;
      try {
        const errorPayload = await response.json();
        message = errorPayload.error?.message || message;
      } catch {
        const text = await response.text();
        message = text || message;
      }
      throw new Error(message);
    }
    if (!response.body) {
      throw new Error("Streaming response body is unavailable.");
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";
    let finalSources = [];
    let finalRequestId = "";

    while (true) {
      const { value, done } = await reader.read();
      if (done) {
        break;
      }

      buffer += decoder.decode(value, { stream: true });
      const blocks = buffer.split(/\n\n/);
      buffer = blocks.pop() || "";
      for (const block of blocks) {
        const event = parseSseBlock(block);
        if (!event) {
          continue;
        }
        if (event.done) {
          break;
        }
        if (event.event === "error") {
          throw new Error(event.payload.error?.message || "Gateway streaming error.");
        }

        const choice = event.payload.choices && event.payload.choices[0];
        const delta = choice ? choice.delta || {} : {};
        if (delta.content) {
          assistant.rawText += delta.content;
          renderAssistantContent(assistant.contentEl, assistant.rawText);
          conversationEl.scrollTop = conversationEl.scrollHeight;
        }
        if (event.payload.rag_request_id) {
          finalRequestId = event.payload.rag_request_id;
          finalSources = event.payload.rag_sources || [];
          requestIdLine.textContent = finalRequestId;
          renderSources(finalSources);
          renderMetadata(event.payload.rag_metadata || {});
          updateAssistantFoot(assistant, finalRequestId, finalSources);
        }
      }
    }

    if (!assistant.contentEl.textContent.trim()) {
      assistant.rawText = "No answer content returned.";
      renderAssistantContent(assistant.contentEl, assistant.rawText);
    }
    if (finalRequestId) {
      updateAssistantFoot(assistant, finalRequestId, finalSources);
    }
  } catch (error) {
    if (error.name === "AbortError") {
      if (!assistant.contentEl.textContent) {
        assistant.rawText = "Stopped.";
        renderAssistantContent(assistant.contentEl, assistant.rawText);
      }
      assistant.footEl.hidden = false;
      assistant.footEl.textContent = "Stopped";
      requestIdLine.textContent = "Stopped";
      detailsTray.hidden = true;
      renderSources(null);
      renderMetadata({});
      return;
    }
    assistant.article.classList.add("error");
    assistant.contentEl.textContent = error.message || "The request failed.";
  } finally {
    state.activeController = null;
    state.activeAssistant = null;
    setBusy(false);
    input.focus();
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const question = input.value.trim();
  if (!question || state.activeController || state.attachmentBusy) {
    return;
  }
  const attachments = attachmentRequestPayload();
  clearAttachments();
  input.value = "";
  resizeComposer();
  streamAnswer(question, attachments);
});

input.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    form.requestSubmit();
  }
});

input.addEventListener("input", resizeComposer);

stopButton.addEventListener("click", () => {
  if (state.activeController) {
    state.activeController.abort();
  }
});

clearButton.addEventListener("click", () => {
  if (state.activeController) {
    state.activeController.abort();
  }
  requestIdLine.textContent = "None";
  detailsTray.hidden = true;
  detailsTray.open = false;
  renderSources(null);
  renderMetadata({});
  clearAttachments();
  renderEmptyChat();
  input.focus();
});

attachButton.addEventListener("click", () => {
  if (!state.attachmentsEnabled) {
    return;
  }
  fileInput.click();
});

fileInput.addEventListener("change", () => {
  addFiles(fileInput.files);
});

themeButton.addEventListener("click", () => {
  applyTheme(state.theme === "dark" ? "light" : "dark", { persist: true });
});

applyTheme(storedTheme() || systemTheme());
renderEmptyChat();
renderSources(null);
renderMetadata({});
renderAttachments();
renderAttachmentPolicy();
resizeComposer();
refreshStatus();
