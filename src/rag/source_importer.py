"""Optional importer for configured HPC documentation sources."""

from __future__ import annotations

import json
import re
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urldefrag, urljoin, urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

from src.rag.source_manifest import CONFIG_PATH, SourceManifest, SourceRecord, source_skip_reasons
from src.rag.source_metadata import metadata_for_source


DEFAULT_USER_AGENT = "oarc-ai-assistant-rag-source-importer/1.0"
DEFAULT_AVOID_TERMS = {
    "account",
    "accounts",
    "mfa",
    "vpn",
    "allocation",
    "allocations",
    "billing",
    "charging",
    "admin",
    "support",
    "helpdesk",
    "queue",
    "queues",
    "partition",
    "partitions",
    "qos",
    "quota",
    "quotas",
    "purge",
    "policy",
    "install",
}


@dataclass
class ImportOptions:
    """Options for dry-run or explicit source import."""

    manifest_path: str | Path = CONFIG_PATH
    group: str = "hpc_additional_docs_first_pass"
    output_dir: str | Path | None = None
    report_dir: str | Path | None = None
    ingest: bool = False
    dry_run: bool = True
    allow_license_pending: bool = False
    max_pages_per_source: int | None = None
    obey_robots_txt: bool | None = None
    user_agent: str = DEFAULT_USER_AGENT
    run_id: str | None = None


@dataclass
class ImportReport:
    """Structured report records emitted by the optional source importer."""

    summary: dict[str, Any] = field(default_factory=dict)
    sources_imported: list[dict[str, Any]] = field(default_factory=list)
    sources_skipped: list[dict[str, Any]] = field(default_factory=list)
    pages_skipped: list[dict[str, Any]] = field(default_factory=list)
    example_only_pages: list[dict[str, Any]] = field(default_factory=list)
    cluster_specific_pages: list[dict[str, Any]] = field(default_factory=list)
    crawl_errors: list[dict[str, Any]] = field(default_factory=list)


def import_sources(
    options: ImportOptions,
    *,
    session: requests.Session | None = None,
) -> ImportReport:
    """Run a dry-run or explicit import for a configured source group."""

    manifest = SourceManifest.from_file(options.manifest_path)
    sources = manifest.resolve_group(options.group)
    defaults = manifest.defaults
    report = ImportReport()

    run_id = options.run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_dir = Path(options.output_dir or defaults.get("output_root") or "docs/corpus/staging")
    report_dir = Path(options.report_dir or defaults.get("report_root") or "logs/rag_source_imports")
    run_report_dir = report_dir / run_id
    max_pages = int(options.max_pages_per_source or defaults.get("max_pages_per_source") or 25)
    obey_robots = (
        bool(defaults.get("obey_robots_txt", True))
        if options.obey_robots_txt is None
        else options.obey_robots_txt
    )
    active_session = session or requests.Session()
    active_session.headers.update({"User-Agent": options.user_agent})
    robots = RobotsCache(active_session, user_agent=options.user_agent, enabled=obey_robots)

    for source in sources:
        skip_reasons = source_skip_reasons(
            source,
            allow_license_pending=options.allow_license_pending,
        )
        if options.dry_run or not options.ingest or skip_reasons:
            report.sources_skipped.append(
                _source_report(
                    source,
                    status="dry_run" if options.dry_run and not skip_reasons else "skipped",
                    reasons=skip_reasons or ["dry_run"],
                )
            )
            continue

        try:
            imported_pages = _import_source(
                source,
                group=options.group,
                output_dir=output_dir,
                session=active_session,
                robots=robots,
                max_pages=max_pages,
                report=report,
            )
            report.sources_imported.append(
                _source_report(source, status="imported", pages_imported=imported_pages)
            )
        except Exception as exc:  # pragma: no cover - defensive reporting path
            report.crawl_errors.append(
                {
                    "source_id": source.source_id,
                    "url": source.public_url,
                    "error_type": exc.__class__.__name__,
                    "message": str(exc),
                }
            )
            report.sources_skipped.append(
                _source_report(source, status="error", reasons=[exc.__class__.__name__])
            )

    report.summary = {
        "run_id": run_id,
        "manifest_path": str(options.manifest_path),
        "group": options.group,
        "dry_run": options.dry_run,
        "ingest": options.ingest,
        "allow_license_pending": options.allow_license_pending,
        "source_count": len(sources),
        "sources_imported": len(report.sources_imported),
        "sources_skipped": len(report.sources_skipped),
        "pages_skipped": len(report.pages_skipped),
        "example_only_pages": len(report.example_only_pages),
        "cluster_specific_pages": len(report.cluster_specific_pages),
        "crawl_errors": len(report.crawl_errors),
        "output_dir": str(output_dir),
        "report_dir": str(run_report_dir),
    }
    write_report(report, run_report_dir)
    return report


class RobotsCache:
    """Small robots.txt cache using the active HTTP session."""

    def __init__(self, session: requests.Session, *, user_agent: str, enabled: bool) -> None:
        self.session = session
        self.user_agent = user_agent
        self.enabled = enabled
        self._cache: dict[str, RobotFileParser | None] = {}

    def can_fetch(self, url: str) -> bool:
        """Return whether robots.txt allows fetching a URL."""

        if not self.enabled:
            return True
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        if base not in self._cache:
            self._cache[base] = self._load(base)
        parser = self._cache[base]
        if parser is None:
            return True
        return parser.can_fetch(self.user_agent, url)

    def _load(self, base: str) -> RobotFileParser | None:
        try:
            response = self.session.get(f"{base}/robots.txt", timeout=20)
        except requests.RequestException:
            return None
        if response.status_code >= 400:
            return None
        parser = RobotFileParser()
        parser.set_url(f"{base}/robots.txt")
        parser.parse(response.text.splitlines())
        return parser


def write_report(report: ImportReport, report_dir: Path) -> None:
    """Persist importer report artifacts."""

    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "summary.json").write_text(
        json.dumps(report.summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _write_jsonl(report_dir / "sources_imported.jsonl", report.sources_imported)
    _write_jsonl(report_dir / "sources_skipped.jsonl", report.sources_skipped)
    _write_jsonl(report_dir / "pages_skipped.jsonl", report.pages_skipped)
    _write_jsonl(report_dir / "example_only_pages.jsonl", report.example_only_pages)
    _write_jsonl(report_dir / "cluster_specific_pages.jsonl", report.cluster_specific_pages)
    _write_jsonl(report_dir / "crawl_errors.jsonl", report.crawl_errors)


def _import_source(
    source: SourceRecord,
    *,
    group: str,
    output_dir: Path,
    session: requests.Session,
    robots: RobotsCache,
    max_pages: int,
    report: ImportReport,
) -> int:
    if source.normalized_ingestion_method == "git_repo":
        raise RuntimeError("git_repo sources require explicit repo_url configuration")

    seen: set[str] = set()
    queue: deque[str] = deque([source.public_url])
    imported = 0
    source_dir = output_dir / source.source_group / source.source_id

    while queue and imported < max_pages:
        url = queue.popleft()
        normalized_url = _normalize_url(url)
        if normalized_url in seen:
            continue
        seen.add(normalized_url)

        allowed, reason = _url_allowed(source, normalized_url, seed=source.public_url)
        if not allowed:
            report.pages_skipped.append(
                {"source_id": source.source_id, "url": normalized_url, "reason": reason}
            )
            continue
        if not robots.can_fetch(normalized_url):
            report.pages_skipped.append(
                {"source_id": source.source_id, "url": normalized_url, "reason": "robots_disallow"}
            )
            continue

        try:
            response = session.get(normalized_url, timeout=60)
            response.raise_for_status()
        except requests.RequestException as exc:
            report.crawl_errors.append(
                {
                    "source_id": source.source_id,
                    "url": normalized_url,
                    "error_type": exc.__class__.__name__,
                    "message": str(exc),
                }
            )
            continue

        content_type = response.headers.get("content-type", "")
        if "html" not in content_type and not normalized_url.endswith((".html", "/")):
            report.pages_skipped.append(
                {"source_id": source.source_id, "url": normalized_url, "reason": "non_html"}
            )
            continue

        page = html_to_markdown(response.text, canonical_url=normalized_url)
        metadata = metadata_for_source(source, canonical_url=normalized_url, content=page["markdown"])
        target = source_dir / _filename_for_url(normalized_url)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(_front_matter(metadata) + page["markdown"], encoding="utf-8")
        imported += 1

        if metadata.get("example_only"):
            report.example_only_pages.append(
                {"source_id": source.source_id, "url": normalized_url, "path": str(target)}
            )
        if metadata.get("cluster_specific"):
            report.cluster_specific_pages.append(
                {
                    "source_id": source.source_id,
                    "url": normalized_url,
                    "path": str(target),
                    "fields": metadata.get("cluster_specific_fields_detected", []),
                }
            )

        if source.normalized_ingestion_method != "controlled_website":
            continue
        for link in _candidate_links(response.text, base_url=normalized_url):
            allowed, reason = _url_allowed(source, link["url"], seed=source.public_url, text=link["text"])
            if allowed and link["url"] not in seen:
                queue.append(link["url"])
            elif not allowed:
                report.pages_skipped.append(
                    {
                        "source_id": source.source_id,
                        "url": link["url"],
                        "reason": reason,
                        "from_url": normalized_url,
                    }
                )

    return imported


def html_to_markdown(html: str, *, canonical_url: str) -> dict[str, str]:
    """Extract main HTML content and convert common structures to Markdown."""

    soup = BeautifulSoup(html, "html.parser")
    main = (
        soup.select_one("main")
        or soup.select_one("article")
        or soup.select_one('[role="main"]')
        or soup.select_one(".rst-content")
        or soup.select_one(".wy-nav-content")
        or soup.select_one(".document")
        or soup.select_one(".content")
        or soup.body
        or soup
    )
    fragment = BeautifulSoup(str(main), "html.parser")
    for tag in fragment.select("script, style, nav, header, footer, form"):
        tag.decompose()
    title_tag = fragment.find(["h1", "title"]) or soup.find("title")
    title = " ".join(title_tag.stripped_strings) if title_tag else canonical_url
    markdown = _node_to_markdown(fragment).strip()
    if title and not markdown.startswith("# "):
        markdown = f"# {title}\n\n{markdown}".strip()
    return {"title": title, "markdown": markdown + "\n"}


def _node_to_markdown(node: Any) -> str:
    parts: list[str] = []
    for child in getattr(node, "children", []) or []:
        name = getattr(child, "name", None)
        if name is None:
            text = str(child)
            if text.strip():
                parts.append(text)
            continue
        if name in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            level = int(name[1])
            parts.append(f"\n{'#' * level} {' '.join(child.stripped_strings)}\n")
        elif name == "p":
            parts.append(f"\n{_inline_text(child)}\n")
        elif name == "pre":
            code = child.get_text("\n").strip("\n")
            parts.append(f"\n```bash\n{code}\n```\n")
        elif name in {"ul", "ol"}:
            ordered = name == "ol"
            for index, item in enumerate(child.find_all("li", recursive=False), start=1):
                bullet = f"{index}." if ordered else "-"
                parts.append(f"{bullet} {_inline_text(item)}\n")
            parts.append("\n")
        elif name == "table":
            parts.append(_table_to_markdown(child))
        elif name in {"blockquote", "div", "section", "article", "main", "body", "html"}:
            parts.append(_node_to_markdown(child))
        elif name == "br":
            parts.append("\n")
        else:
            text = _inline_text(child)
            if text:
                parts.append(text)
    return _clean_markdown("".join(parts))


def _inline_text(node: Any) -> str:
    for code in node.find_all("code"):
        code.string = f"`{code.get_text(strip=True)}`"
    for link in node.find_all("a", href=True):
        label = " ".join(link.stripped_strings) or link["href"]
        link.string = f"[{label}]({link['href']})"
    return " ".join(node.get_text(" ", strip=True).split())


def _table_to_markdown(table: Any) -> str:
    rows = []
    for row in table.find_all("tr"):
        cells = [" ".join(cell.get_text(" ", strip=True).split()) for cell in row.find_all(["th", "td"])]
        if cells:
            rows.append(cells)
    if not rows:
        return ""
    width = max(len(row) for row in rows)
    normalized = [row + [""] * (width - len(row)) for row in rows]
    header = normalized[0]
    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join("---" for _ in header) + " |",
    ]
    for row in normalized[1:]:
        lines.append("| " + " | ".join(row) + " |")
    return "\n" + "\n".join(lines) + "\n"


def _candidate_links(html: str, *, base_url: str) -> list[dict[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for anchor in soup.find_all("a", href=True):
        href = anchor["href"].strip()
        if not href or href.startswith(("mailto:", "tel:", "javascript:")):
            continue
        links.append(
            {
                "url": _normalize_url(urljoin(base_url, href)),
                "text": " ".join(anchor.stripped_strings),
            }
        )
    return links


def _url_allowed(
    source: SourceRecord,
    url: str,
    *,
    seed: str,
    text: str = "",
) -> tuple[bool, str]:
    parsed_seed = urlparse(seed)
    parsed_url = urlparse(url)
    if parsed_url.scheme not in {"http", "https"}:
        return False, "unsupported_scheme"
    if parsed_url.netloc != parsed_seed.netloc:
        return False, "different_domain"

    haystack = f"{url} {text}".lower()
    include_rules = [rule.lower() for rule in source.include_rules]
    if _normalize_url(url) != _normalize_url(seed) and include_rules:
        if not any(_rule_matches(rule, haystack) for rule in include_rules):
            return False, "not_in_include_rules"

    for rule in source.exclude_rules:
        if _rule_matches(rule.lower(), haystack):
            return False, "exclude_rule"

    explicit_includes = " ".join(include_rules)
    if _normalize_url(url) != _normalize_url(seed):
        for term in DEFAULT_AVOID_TERMS:
            if term in haystack and term not in explicit_includes:
                return False, "default_cluster_policy_exclude"

    return True, ""


def _rule_matches(rule: str, haystack: str) -> bool:
    if not rule:
        return False
    normalized_rule = re.sub(r"[^a-z0-9./_-]+", " ", rule.lower()).strip()
    if not normalized_rule:
        return False
    return normalized_rule in haystack or all(part in haystack for part in normalized_rule.split())


def _normalize_url(url: str) -> str:
    clean, _ = urldefrag(url)
    parsed = urlparse(clean)
    path = parsed.path or "/"
    return parsed._replace(path=path).geturl()


def _filename_for_url(url: str) -> Path:
    parsed = urlparse(url)
    slug = parsed.path.strip("/").replace("/", "__") or "index"
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", slug).strip("-") or "index"
    if slug.endswith(".html"):
        slug = slug[:-5]
    return Path(f"{slug}.md")


def _front_matter(metadata: dict[str, Any]) -> str:
    lines = ["---"]
    for key in sorted(metadata):
        value = metadata[key]
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {json.dumps(item)}")
        elif isinstance(value, bool):
            lines.append(f"{key}: {'true' if value else 'false'}")
        elif isinstance(value, (int, float)):
            lines.append(f"{key}: {value}")
        elif value is None:
            lines.append(f"{key}: null")
        else:
            lines.append(f"{key}: {json.dumps(str(value))}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def _clean_markdown(text: str) -> str:
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def _source_report(
    source: SourceRecord,
    *,
    status: str,
    reasons: list[str] | None = None,
    pages_imported: int = 0,
) -> dict[str, Any]:
    return {
        "source_id": source.source_id,
        "title": source.title,
        "url": source.public_url,
        "source_group": source.source_group,
        "normalized_ingestion_method": source.normalized_ingestion_method,
        "decision": source.decision,
        "status": status,
        "reasons": reasons or [],
        "pages_imported": pages_imported,
        "license_review_required": source.license_review_required,
        "license_note": source.license_note,
    }


def _write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(record, sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )


__all__ = [
    "ImportOptions",
    "ImportReport",
    "RobotsCache",
    "html_to_markdown",
    "import_sources",
    "write_report",
]
