"""Deterministic gateway safety guards for requests the model should not answer."""

from __future__ import annotations

import re

_RAW_TICKET_RE = re.compile(
    r"\b(raw|print|dump|show|export|reveal).{0,80}\b(ticket|servicenow|private fields?)\b",
    re.IGNORECASE,
)
_PASSWORD_RE = re.compile(
    r"\b(shared|admin|root|cluster|amarel).{0,60}\b(password|passphrase|secret)\b",
    re.IGNORECASE,
)
_PROMPT_SECRET_RE = re.compile(
    r"\b(hidden|system).{0,40}\b(prompt|instructions?)\b|\b(api[_ -]?key|secret key)\b",
    re.IGNORECASE,
)

_REFUSAL = (
    "I can't provide raw ticket data, private records, passwords, secrets, or hidden prompts. "
    "For access to support records or account help, contact the OARC helpdesk through the "
    "approved support process."
)


def safety_refusal_for_question(question: str) -> str | None:
    """Return a deterministic refusal for sensitive data-exfiltration requests."""

    text = str(question or "")
    if _RAW_TICKET_RE.search(text) or _PASSWORD_RE.search(text) or _PROMPT_SECRET_RE.search(text):
        return _REFUSAL
    return None


__all__ = ["safety_refusal_for_question"]
