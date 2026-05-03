"""Import official Slurm source documentation into a RAG-ready corpus tree."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import tarfile
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader

from src.rag.logger import get_logger

logger = get_logger(__name__)

ARCHIVE_BASE_URL = "https://download.schedmd.com/slurm"
CANONICAL_BASE_URL = "https://slurm.schedmd.com/"
HOME_PAGE = PurePosixPath("slurm.html")
INCLUDE_REGEX = re.compile(r'<!--\s*#include\s*virtual\s*=\s*"([^"]+)"\s*-->')
VERSION_REGEX = re.compile(r"@SLURM_VERSION@")
PAGE_TITLE_REGEX = re.compile(r"<!--\s*#pagetitle\s*-->")
CANONICAL_REGEX = re.compile(r"<!--\s*#canonical\s*-->")
MAN_PAGE_SUFFIXES = {".1", ".5", ".8"}
HTML_PARSER = "lxml" if importlib.util.find_spec("lxml") else "html.parser"


@dataclass(frozen=True)
class ArchiveMetadata:
    """Metadata about the imported source archive."""

    path: Path
    size_bytes: int
    sha256: str
    source_url: str


def build_source_url(version: str) -> str:
    """Return the official Slurm source archive URL for a version."""
    return f"{ARCHIVE_BASE_URL}/slurm-{version}.tar.bz2"


def import_slurm_docs(
    version: str = "23.02.7",
    output_dir: str | Path = "docs/slurm-23.02.7",
    *,
    force: bool = False,
    archive_path: str | Path | None = None,
    source_url: str | None = None,
) -> dict[str, Any]:
    """Download or read a Slurm archive and build a local corpus tree.

    Args:
        version: Slurm release version.
        output_dir: Destination directory for the generated corpus.
        force: Replace an existing destination directory when True.
        archive_path: Optional local tarball path. Tests use this to avoid
            network access.
        source_url: Optional provenance URL written into the manifest.

    Returns:
        The generated manifest dictionary.
    """

    _ensure_pandoc_available()

    destination = Path(output_dir)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and not force:
        raise FileExistsError(
            f"{destination} already exists. Re-run with --force to replace it."
        )
    if destination.exists() and not destination.is_dir():
        raise NotADirectoryError(f"{destination} exists and is not a directory.")

    provenance_url = source_url or (
        Path(archive_path).resolve().as_uri() if archive_path else build_source_url(version)
    )
    logger.info("Importing Slurm docs %s into %s", version, destination)

    with tempfile.TemporaryDirectory(
        dir=destination.parent,
        prefix=f".{destination.name}.tmp-",
    ) as temp_dir:
        temp_root = Path(temp_dir)
        work_root = temp_root / destination.name
        upstream_html_dir = work_root / "upstream" / "html"
        upstream_man_dir = work_root / "upstream" / "man"
        rendered_html_dir = work_root / "rendered" / "html"
        markdown_html_dir = work_root / "markdown" / "html"
        markdown_man_dir = work_root / "markdown" / "man"
        markdown_pdf_dir = work_root / "markdown" / "pdf"

        archive = _prepare_archive(
            temp_root=temp_root,
            version=version,
            archive_path=archive_path,
            source_url=provenance_url,
        )

        _extract_tree(
            archive.path,
            prefix=f"slurm-{version}/doc/html/",
            destination=upstream_html_dir,
        )
        _extract_tree(
            archive.path,
            prefix=f"slurm-{version}/doc/man/",
            destination=upstream_man_dir,
        )

        html_page_count = _render_html_tree(
            upstream_html_dir=upstream_html_dir,
            rendered_html_dir=rendered_html_dir,
            markdown_html_dir=markdown_html_dir,
            version=version,
        )
        pdf_count = _convert_pdf_tree(
            upstream_html_dir=upstream_html_dir,
            markdown_pdf_dir=markdown_pdf_dir,
        )
        man_page_count = _convert_man_tree(
            upstream_man_dir=upstream_man_dir,
            markdown_man_dir=markdown_man_dir,
        )

        manifest = {
            "slurm_version": version,
            "source_url": archive.source_url,
            "archive_size_bytes": archive.size_bytes,
            "archive_sha256": archive.sha256,
            "imported_at": datetime.now(timezone.utc).isoformat(),
            "raw_html_file_count": _count_files(upstream_html_dir),
            "raw_man_file_count": _count_files(upstream_man_dir),
            "web_doc_count": html_page_count + pdf_count,
            "html_page_count": html_page_count,
            "markdown_html_count": html_page_count,
            "pdf_count": pdf_count,
            "markdown_pdf_count": pdf_count,
            "man_page_count": man_page_count,
            "markdown_man_count": man_page_count,
        }

        _write_text(work_root / "manifest.json", json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        _write_text(work_root / "README.md", _build_corpus_readme(destination=destination, manifest=manifest))

        if destination.exists():
            shutil.rmtree(destination)
        shutil.move(str(work_root), str(destination))

    logger.info(
        "Imported Slurm %s corpus: %s html pages, %s PDFs, %s man pages",
        version,
        manifest["html_page_count"],
        manifest["pdf_count"],
        manifest["man_page_count"],
    )
    return manifest


def _prepare_archive(
    *,
    temp_root: Path,
    version: str,
    archive_path: str | Path | None,
    source_url: str,
) -> ArchiveMetadata:
    if archive_path is None:
        archive_file = temp_root / f"slurm-{version}.tar.bz2"
        _download_archive(source_url, archive_file)
    else:
        archive_file = Path(archive_path)
        if not archive_file.exists():
            raise FileNotFoundError(f"Archive does not exist: {archive_file}")

    return ArchiveMetadata(
        path=archive_file,
        size_bytes=archive_file.stat().st_size,
        sha256=_sha256_file(archive_file),
        source_url=source_url,
    )


def _download_archive(url: str, destination: Path) -> None:
    logger.info("Downloading Slurm archive from %s", url)
    response = requests.get(url, timeout=120)
    response.raise_for_status()
    destination.write_bytes(response.content)


def _extract_tree(archive_path: Path, *, prefix: str, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive_path, "r:bz2") as archive:
        for member in archive.getmembers():
            relative_path = _member_relative_path(member.name, prefix)
            if relative_path is None:
                continue
            target = destination / relative_path
            if member.isdir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            if not member.isfile():
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            extracted = archive.extractfile(member)
            if extracted is None:
                continue
            with extracted, target.open("wb") as handle:
                shutil.copyfileobj(extracted, handle)


def _render_html_tree(
    *,
    upstream_html_dir: Path,
    rendered_html_dir: Path,
    markdown_html_dir: Path,
    version: str,
) -> int:
    rendered_html_dir.mkdir(parents=True, exist_ok=True)
    markdown_html_dir.mkdir(parents=True, exist_ok=True)

    html_pages = 0
    for source_file in sorted(upstream_html_dir.rglob("*")):
        if not source_file.is_file():
            continue
        relative_path = PurePosixPath(source_file.relative_to(upstream_html_dir).as_posix())
        if relative_path.suffix == ".shtml":
            rendered_relative = relative_path.with_suffix(".html")
            rendered_html = _render_html_page(
                source_path=source_file,
                source_relative=relative_path,
                rendered_relative=rendered_relative,
                version=version,
            )
            _write_text(rendered_html_dir / Path(rendered_relative), rendered_html)
            markdown = _convert_rendered_html_to_markdown(
                rendered_html=rendered_html,
                current_rendered_relative=rendered_relative,
            )
            _write_text(markdown_html_dir / Path(rendered_relative.with_suffix(".md")), markdown)
            html_pages += 1
            continue

        target_file = rendered_html_dir / source_file.relative_to(upstream_html_dir)
        target_file.parent.mkdir(parents=True, exist_ok=True)

        if relative_path.suffix == ".html":
            rendered_html = _rewrite_rendered_html(
                html_text=source_file.read_text(encoding="utf-8"),
                current_relative=relative_path,
            )
            _write_text(target_file, rendered_html)
            markdown = _convert_rendered_html_to_markdown(
                rendered_html=rendered_html,
                current_rendered_relative=relative_path,
            )
            _write_text(markdown_html_dir / Path(relative_path.with_suffix(".md")), markdown)
            html_pages += 1
            continue

        shutil.copy2(source_file, target_file)
        if relative_path.suffix.lower() != ".pdf":
            markdown_asset = markdown_html_dir / source_file.relative_to(upstream_html_dir)
            markdown_asset.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_file, markdown_asset)

    return html_pages


def _convert_pdf_tree(*, upstream_html_dir: Path, markdown_pdf_dir: Path) -> int:
    markdown_pdf_dir.mkdir(parents=True, exist_ok=True)
    converted = 0
    for pdf_path in sorted(upstream_html_dir.rglob("*.pdf")):
        relative_path = PurePosixPath(pdf_path.relative_to(upstream_html_dir).as_posix())
        markdown = _convert_pdf_to_markdown(pdf_path)
        _write_text(markdown_pdf_dir / Path(relative_path.with_suffix(".md")), markdown)
        converted += 1
    return converted


def _convert_man_tree(*, upstream_man_dir: Path, markdown_man_dir: Path) -> int:
    markdown_man_dir.mkdir(parents=True, exist_ok=True)
    converted = 0
    for man_path in sorted(upstream_man_dir.rglob("*")):
        if not man_path.is_file() or man_path.suffix not in MAN_PAGE_SUFFIXES:
            continue
        relative_path = PurePosixPath(man_path.relative_to(upstream_man_dir).as_posix())
        markdown = _run_pandoc(man_path.read_text(encoding="utf-8"), from_format="man")
        _write_text(markdown_man_dir / Path(relative_path.with_suffix(".md")), markdown)
        converted += 1
    return converted


def _render_html_page(
    *,
    source_path: Path,
    source_relative: PurePosixPath,
    rendered_relative: PurePosixPath,
    version: str,
) -> str:
    source_text = source_path.read_text(encoding="utf-8")
    expanded = _expand_virtual_includes(source_path, source_text)
    title = _extract_title(expanded, fallback=source_path.stem.replace("_", " "))
    expanded = PAGE_TITLE_REGEX.sub(
        f"<title>Slurm Workload Manager - {title}</title>",
        expanded,
    )
    expanded = CANONICAL_REGEX.sub(
        f'<link rel="canonical" href="{CANONICAL_BASE_URL}{rendered_relative.as_posix()}">',
        expanded,
    )
    expanded = VERSION_REGEX.sub(version, expanded)
    return _rewrite_rendered_html(html_text=expanded, current_relative=source_relative)


def _rewrite_rendered_html(*, html_text: str, current_relative: PurePosixPath) -> str:
    soup = BeautifulSoup(html_text, HTML_PARSER)
    current_rendered = (
        current_relative.with_suffix(".html")
        if current_relative.suffix == ".shtml"
        else current_relative
    )

    for tag in soup.find_all(href=True):
        rewritten = _rewrite_rendered_href(tag["href"], current_rendered=current_rendered)
        if rewritten is not None:
            tag["href"] = rewritten

    return str(soup)


def _rewrite_rendered_href(href: str, *, current_rendered: PurePosixPath) -> str | None:
    target = _resolve_local_doc_target(href, current_relative=current_rendered)
    if target is None:
        return None
    target_path, fragment = target
    if target_path.suffix.lower() == ".shtml":
        target_path = target_path.with_suffix(".html")
    if target_path == HOME_PAGE:
        target_path = HOME_PAGE
    return _relative_href(current_rendered, target_path, fragment)


def _convert_rendered_html_to_markdown(
    *,
    rendered_html: str,
    current_rendered_relative: PurePosixPath,
) -> str:
    fragment = _extract_markdown_fragment(
        rendered_html=rendered_html,
        current_rendered_relative=current_rendered_relative,
    )
    return _run_pandoc(fragment, from_format="html")


def _extract_markdown_fragment(
    *,
    rendered_html: str,
    current_rendered_relative: PurePosixPath,
) -> str:
    soup = BeautifulSoup(rendered_html, HTML_PARSER)
    main = soup.select_one('div.content[role="main"]') or soup.body or soup

    fragment = BeautifulSoup("<html><body></body></html>", HTML_PARSER)
    for child in list(main.contents):
        fragment.body.append(child.extract())

    for tag in fragment.select("script, style, .slurm-search, .site-header, .site-footer, nav"):
        tag.decompose()
    for tag in fragment.select("a.slurm_link"):
        tag.decompose()

    current_markdown = PurePosixPath("html") / current_rendered_relative.with_suffix(".md")
    for tag in fragment.find_all(href=True):
        rewritten = _rewrite_markdown_href(
            tag["href"],
            current_rendered_relative=current_rendered_relative,
            current_markdown_relative=current_markdown,
        )
        if rewritten is not None:
            tag["href"] = rewritten

    for block in list(fragment.body.find_all("div")):
        block.unwrap()

    return str(fragment)


def _rewrite_markdown_href(
    href: str,
    *,
    current_rendered_relative: PurePosixPath,
    current_markdown_relative: PurePosixPath,
) -> str | None:
    target = _resolve_local_doc_target(href, current_relative=current_rendered_relative)
    if target is None:
        return None

    target_path, fragment = target
    suffix = target_path.suffix.lower()
    if suffix in {".html", ".shtml"}:
        markdown_target = PurePosixPath("html") / target_path.with_suffix(".md")
    elif suffix == ".pdf":
        markdown_target = PurePosixPath("pdf") / target_path.with_suffix(".md")
    else:
        return None
    return _relative_href(current_markdown_relative, markdown_target, fragment)


def _resolve_local_doc_target(
    href: str,
    *,
    current_relative: PurePosixPath,
) -> tuple[PurePosixPath, str] | None:
    parsed = urlparse(href)

    if parsed.scheme:
        if parsed.scheme not in {"http", "https"} or parsed.netloc != "slurm.schedmd.com":
            return None
        if not parsed.path or parsed.path == "/":
            target_path = HOME_PAGE
        else:
            target_path = _normalize_posix(PurePosixPath(parsed.path.lstrip("/")))
    else:
        raw_path = parsed.path
        if not raw_path:
            target_path = current_relative
        elif raw_path == "/":
            target_path = HOME_PAGE
        elif raw_path.startswith("/"):
            target_path = _normalize_posix(PurePosixPath(raw_path.lstrip("/")))
        else:
            target_path = _normalize_posix(current_relative.parent / PurePosixPath(raw_path))

    return target_path, parsed.fragment


def _normalize_posix(path: PurePosixPath) -> PurePosixPath:
    parts: list[str] = []
    for part in path.parts:
        if part in {"", "."}:
            continue
        if part == "..":
            if parts:
                parts.pop()
            continue
        parts.append(part)
    return PurePosixPath(*parts)


def _relative_href(current_relative: PurePosixPath, target_relative: PurePosixPath, fragment: str) -> str:
    if current_relative == target_relative and fragment:
        return f"#{fragment}"
    relative = os.path.relpath(
        str(target_relative),
        start=str(current_relative.parent),
    ).replace(os.sep, "/")
    return f"{relative}#{fragment}" if fragment else relative


def _expand_virtual_includes(
    source_path: Path,
    text: str,
    *,
    seen: set[Path] | None = None,
) -> str:
    visited = set(seen or set())

    def include_replacement(match: re.Match[str]) -> str:
        include_name = match.group(1)
        include_path = (source_path.parent / include_name).resolve()
        if include_path in visited or not include_path.exists():
            return match.group(0)
        include_text = include_path.read_text(encoding="utf-8")
        return _expand_virtual_includes(
            include_path,
            include_text,
            seen=visited | {include_path},
        )

    return INCLUDE_REGEX.sub(include_replacement, text)


def _extract_title(html_text: str, *, fallback: str) -> str:
    soup = BeautifulSoup(html_text, HTML_PARSER)
    heading = soup.find("h1")
    if heading is None:
        return fallback
    title = " ".join(heading.stripped_strings)
    return title or fallback


def _convert_pdf_to_markdown(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    metadata_title = getattr(reader.metadata, "title", None) if reader.metadata else None
    title = metadata_title or pdf_path.stem.replace("_", " ")

    body_parts = []
    for page in reader.pages:
        extracted = (page.extract_text() or "").strip()
        if extracted:
            body_parts.append(extracted)
    body = "\n\n".join(body_parts).strip()
    if not body:
        body = "Text extraction did not return any content for this PDF."

    return f"# {title}\n\n{body}\n"


def _run_pandoc(text: str, *, from_format: str) -> str:
    result = subprocess.run(
        [
            "pandoc",
            "-f",
            from_format,
            "-t",
            "gfm",
            "--wrap=auto",
            "--columns=100",
        ],
        input=text,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"pandoc failed for {from_format}: {result.stderr.strip()}")
    return result.stdout.strip() + "\n"


def _ensure_pandoc_available() -> None:
    if shutil.which("pandoc") is None:
        raise RuntimeError("pandoc is required to import Slurm docs.")


def _member_relative_path(member_name: str, prefix: str) -> Path | None:
    if not member_name.startswith(prefix):
        return None
    relative = member_name[len(prefix) :].lstrip("/")
    if not relative:
        return None
    pure = PurePosixPath(relative)
    if pure.is_absolute() or ".." in pure.parts:
        raise ValueError(f"Unsafe archive path: {member_name}")
    return Path(*pure.parts)


def _count_files(root: Path) -> int:
    return sum(1 for path in root.rglob("*") if path.is_file())


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _build_corpus_readme(*, destination: Path, manifest: dict[str, Any]) -> str:
    output_display = destination.as_posix()
    imported_at = manifest["imported_at"]
    source_url = manifest["source_url"]
    sha256 = manifest["archive_sha256"]
    return (
        "# Slurm 23.02.7 Corpus\n\n"
        "This directory vendors the official Slurm 23.02.7 documentation for local retrieval and offline "
        "inspection.\n\n"
        "## Provenance\n"
        f"- Source archive: {source_url}\n"
        f"- Imported at: {imported_at}\n"
        f"- Archive SHA256: `{sha256}`\n"
        f"- Archive size: {manifest['archive_size_bytes']} bytes\n\n"
        "## Layout\n"
        "- `upstream/html` and `upstream/man`: exact extracted upstream docs\n"
        "- `rendered/html`: SSI-expanded browseable HTML\n"
        "- `markdown/html`, `markdown/man`, `markdown/pdf`: Markdown corpus for the loader\n"
        "- `manifest.json`: import metadata and counts\n\n"
        "## Counts\n"
        f"- Web docs: {manifest['web_doc_count']} "
        f"({manifest['html_page_count']} HTML pages + {manifest['pdf_count']} PDFs)\n"
        f"- Man pages: {manifest['man_page_count']}\n"
        f"- Raw upstream HTML files: {manifest['raw_html_file_count']}\n"
        f"- Raw upstream man files: {manifest['raw_man_file_count']}\n\n"
        "## Using This Corpus\n"
        f"- Runtime: `DATA_PATH={output_display}/markdown`\n"
        f"- Evaluation: set `dataset.document_source.markdown_dir: \"{output_display}/markdown\"`\n"
        "- The default corpus remains `docs/google_sites_guide`.\n\n"
        "## Rebuild Command\n"
        f"- `python scripts/rag/import_slurm_docs.py --version 23.02.7 --output-dir {output_display} --force`\n"
    )


__all__ = ["build_source_url", "import_slurm_docs"]
