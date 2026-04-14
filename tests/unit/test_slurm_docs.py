from __future__ import annotations

import base64
import io
import shutil
import tarfile
from pathlib import Path

import pytest

from src.rag.slurm_docs import build_source_url, import_slurm_docs

PDF_FIXTURE_B64 = (
    "JVBERi0xLjMKJZOMi54gUmVwb3J0TGFiIEdlbmVyYXRlZCBQREYgZG9jdW1lbnQgaHR0cDovL3d3dy5yZXBvcnRs"
    "YWIuY29tCjEgMCBvYmoKPDwKL0YxIDIgMCBSCj4+CmVuZG9iagoyIDAgb2JqCjw8Ci9CYXNlRm9udCAvSGVsdmV0"
    "aWNhIC9FbmNvZGluZyAvV2luQW5zaUVuY29kaW5nIC9OYW1lIC9GMSAvU3VidHlwZSAvVHlwZTEgL1R5cGUgL0Zv"
    "bnQKPj4KZW5kb2JqCjMgMCBvYmoKPDwKL0NvbnRlbnRzIDcgMCBSIC9NZWRpYUJveCBbIDAgMCA1OTUuMjc1NiA4"
    "NDEuODg5OCBdIC9QYXJlbnQgNiAwIFIgL1Jlc291cmNlcyA8PAovRm9udCAxIDAgUiAvUHJvY1NldCBbIC9QREYg"
    "L1RleHQgL0ltYWdlQiAvSW1hZ2VDIC9JbWFnZUkgXQo+PiAvUm90YXRlIDAgL1RyYW5zIDw8Cgo+PiAKICAvVHlw"
    "ZSAvUGFnZQo+PgplbmRvYmoKNCAwIG9iago8PAovUGFnZU1vZGUgL1VzZU5vbmUgL1BhZ2VzIDYgMCBSIC9UeXBl"
    "IC9DYXRhbG9nCj4+CmVuZG9iago1IDAgb2JqCjw8Ci9BdXRob3IgKGFub255bW91cykgL0NyZWF0aW9uRGF0ZSAo"
    "RDoyMDI2MDMyNzE2MTg0Ny0wNCcwMCcpIC9DcmVhdG9yIChSZXBvcnRMYWIgUERGIExpYnJhcnkgLSB3d3cucmVw"
    "b3J0bGFiLmNvbSkgL0tleXdvcmRzICgpIC9Nb2REYXRlIChEOjIwMjYwMzI3MTYxODQ3LTA0JzAwJykgL1Byb2R1"
    "Y2VyIChSZXBvcnRMYWIgUERGIExpYnJhcnkgLSB3d3cucmVwb3J0bGFiLmNvbSkgCiAgL1N1YmplY3QgKHVuc3Bl"
    "Y2lmaWVkKSAvVGl0bGUgKHVudGl0bGVkKSAvVHJhcHBlZCAvRmFsc2UKPj4KZW5kb2JqCjYgMCBvYmoKPDwKL0Nv"
    "dW50IDEgL0tpZHMgWyAzIDAgUiBdIC9UeXBlIC9QYWdlcwo+PgplbmRvYmoKNyAwIG9iago8PAovRmlsdGVyIFsg"
    "L0FTQ0lJODVEZWNvZGUgL0ZsYXRlRGVjb2RlIF0gL0xlbmd0aCAxMTEKPj4Kc3RyZWFtCkdhcFFoMEU9RiwwVVxI"
    "M1RccE5ZVF5RS2s/dGM+SVAsO1cjVTFeMjNpaFBFTV8/Q1c0S0lTaTwhWzdgI09CX3F1XCcwX21kXDldcCEjSVNK"
    "alNaWlJlQFpEZ0tvZGo+JjFydGIiWUtlaWFWRXR+PmVuZHN0cmVhbQplbmRvYmoKeHJlZgowIDgKMDAwMDAwMDAw"
    "MCA2NTUzNSBmIAowMDAwMDAwMDczIDAwMDAwIG4gCjAwMDAwMDAxMDQgMDAwMDAgbiAKMDAwMDAwMDIxMSAwMDAw"
    "MCBuIAowMDAwMDAwNDE0IDAwMDAwIG4gCjAwMDAwMDA0ODIgMDAwMDAgbiAKMDAwMDAwMDc3OCAwMDAwMCBuIAow"
    "MDAwMDAwODM3IDAwMDAwIG4gCnRyYWlsZXIKPDwKL0lEIApbPDZjNDE3ZThhMWFhMGYyMWI1MmFlOTYxMTJiNzg3"
    "MWU1Pjw2YzQxN2U4YTFhYTBmMjFiNTJhZTk2MTEyYjc4NzFlNT5dCiUgUmVwb3J0TGFiIGdlbmVyYXRlZCBQREYg"
    "ZG9jdW1lbnQgLS0gZGlnZXN0IChodHRwOi8vd3d3LnJlcG9ydGxhYi5jb20pCgovSW5mbyA1IDAgUgovUm9vdCA0"
    "IDAgUgovU2l6ZSA4Cj4+CnN0YXJ0eHJlZgoxMDM4CiUlRU9GCg=="
)

PANDOC_UNAVAILABLE = shutil.which("pandoc") is None


def _build_fixture_archive(path: Path) -> None:
    with tarfile.open(path, "w:bz2") as archive:
        _add_text_file(
            archive,
            "slurm-23.02.7/doc/html/header.txt",
            """<!DOCTYPE html>
<html lang="en-US">
<head>
<!--#pagetitle-->
<!--#canonical-->
</head>
<body>
<header class="site-header"><a href="/">Home</a></header>
<div class="content" role="main">
<div class="section slurm-search"><div id="cse"></div></div>
<div class="section"><div class="container">
""",
        )
        _add_text_file(
            archive,
            "slurm-23.02.7/doc/html/footer.txt",
            """
</div></div></div>
<footer class="site-footer">Footer</footer>
</body>
</html>
""",
        )
        _add_text_file(
            archive,
            "slurm-23.02.7/doc/html/quickstart.shtml",
            """<!--#include virtual="header.txt"-->
<h1>Quick Start Guide</h1>
<p><a href="release.html#notes">Release notes</a></p>
<p><a href="manual.pdf">PDF manual</a></p>
<p><img src="diagram.png" alt="Diagram"></p>
<h2 id="overview">Overview<a class="slurm_link" href="#overview"></a></h2>
<p>Quickstart content.</p>
<!--#include virtual="footer.txt"-->
""",
        )
        _add_text_file(
            archive,
            "slurm-23.02.7/doc/html/release.html",
            """<html><body><div class="content" role="main"><h1>Release Notes</h1>
<p id="notes">Stable notes.</p></div></body></html>
""",
        )
        _add_binary_file(
            archive,
            "slurm-23.02.7/doc/html/manual.pdf",
            base64.b64decode(PDF_FIXTURE_B64),
        )
        _add_binary_file(
            archive,
            "slurm-23.02.7/doc/html/diagram.png",
            b"fake-png",
        )
        _add_text_file(
            archive,
            "slurm-23.02.7/doc/man/man1/sbatch.1",
            """.TH SBATCH 1 "Fixture"
.SH NAME
sbatch \\- Submit a batch script to Slurm.
.SH DESCRIPTION
sbatch submits a batch script to Slurm.
""",
        )


def _add_text_file(archive: tarfile.TarFile, name: str, text: str) -> None:
    encoded = text.encode("utf-8")
    info = tarfile.TarInfo(name=name)
    info.size = len(encoded)
    archive.addfile(info, io.BytesIO(encoded))


def _add_binary_file(archive: tarfile.TarFile, name: str, data: bytes) -> None:
    info = tarfile.TarInfo(name=name)
    info.size = len(data)
    archive.addfile(info, io.BytesIO(data))


def test_build_source_url():
    assert build_source_url("23.02.7") == "https://download.schedmd.com/slurm/slurm-23.02.7.tar.bz2"


@pytest.mark.skipif(PANDOC_UNAVAILABLE, reason="pandoc is required for Slurm import tests")
def test_import_slurm_docs_from_local_archive(tmp_path: Path):
    archive_path = tmp_path / "slurm-23.02.7.tar.bz2"
    _build_fixture_archive(archive_path)
    output_dir = tmp_path / "docs" / "slurm-23.02.7"

    manifest = import_slurm_docs(
        version="23.02.7",
        output_dir=output_dir,
        archive_path=archive_path,
        source_url="file:///fixture/slurm-23.02.7.tar.bz2",
    )

    assert manifest["html_page_count"] == 2
    assert manifest["pdf_count"] == 1
    assert manifest["man_page_count"] == 1
    assert manifest["web_doc_count"] == 3

    quickstart = (output_dir / "markdown" / "html" / "quickstart.md").read_text(encoding="utf-8")
    assert "# Quick Start Guide" in quickstart
    assert "(release.md#notes)" in quickstart
    assert "(../pdf/manual.md)" in quickstart
    assert "Quickstart content." in quickstart
    assert "site-header" not in quickstart

    release_notes = (output_dir / "markdown" / "html" / "release.md").read_text(encoding="utf-8")
    assert "# Release Notes" in release_notes

    manual = (output_dir / "markdown" / "pdf" / "manual.md").read_text(encoding="utf-8")
    assert "Fixture PDF content" in manual

    sbatch = (output_dir / "markdown" / "man" / "man1" / "sbatch.md").read_text(encoding="utf-8")
    assert "# NAME" in sbatch
    assert "Submit a batch script to Slurm" in sbatch

    assert (output_dir / "rendered" / "html" / "quickstart.html").exists()
    assert (output_dir / "upstream" / "html" / "manual.pdf").exists()
    assert (output_dir / "markdown" / "html" / "diagram.png").exists()

    corpus_readme = (output_dir / "README.md").read_text(encoding="utf-8")
    assert "DATA_PATH=" in corpus_readme
    assert "file:///fixture/slurm-23.02.7.tar.bz2" in corpus_readme


@pytest.mark.skipif(PANDOC_UNAVAILABLE, reason="pandoc is required for Slurm import tests")
def test_import_slurm_docs_requires_force_to_overwrite(tmp_path: Path):
    archive_path = tmp_path / "slurm-23.02.7.tar.bz2"
    _build_fixture_archive(archive_path)
    output_dir = tmp_path / "docs" / "slurm-23.02.7"
    output_dir.mkdir(parents=True)

    with pytest.raises(FileExistsError):
        import_slurm_docs(
            version="23.02.7",
            output_dir=output_dir,
            archive_path=archive_path,
            source_url="file:///fixture/slurm-23.02.7.tar.bz2",
        )
