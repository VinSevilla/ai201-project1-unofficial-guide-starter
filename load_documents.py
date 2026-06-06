"""
load_documents.py
=================

The very FIRST stage of "The Unofficial CS Career Guide" RAG pipeline:
load every local document from disk and save it to a consistent format
*before any cleaning happens*.

Why a separate step?
    Keeping a raw, untouched copy gives you a stable starting point. If you
    later change how you clean or chunk, you can always re-run from this raw
    snapshot instead of re-reading and re-parsing the original files. It also
    makes debugging easy: you can compare "raw" vs "cleaned" side by side.

What it does:
    1. Read every .txt file in the documents/ folder.
    2. Pull out the title, URL, and source type from each file's header block.
    3. Keep the document body EXACTLY as-is (no whitespace or clutter cleaning).
    4. Save all documents to raw_documents.json in one consistent shape.
    5. Print a short summary so you can confirm all files loaded.

The cleaning + chunking script (ingest_and_chunk.py) is the next stage and can
read from this file.
"""

import json
import re
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DOCUMENTS_DIR = Path("documents")          # where the .txt source files live
OUTPUT_FILE = Path("raw_documents.json")   # where the raw snapshot is written


# ---------------------------------------------------------------------------
# Header parsing (each file opens with a metadata comment block)
# ---------------------------------------------------------------------------

# Each source file starts with a header comment block like:
#   <!--
#   # TITLE: Some title here
#   # URL: https://example.com/...
#   -->
HEADER_BLOCK_RE = re.compile(r"<!--.*?-->", re.DOTALL)
TITLE_RE = re.compile(r"#\s*TITLE:\s*(.+)", re.IGNORECASE)
URL_RE = re.compile(r"#\s*URL:\s*(\S+)", re.IGNORECASE)

# Map a domain fragment to a human-readable source type. First match wins,
# so list the most specific domains first.
SOURCE_TYPE_BY_DOMAIN = [
    ("reddit.com", "Reddit discussion"),
    ("stackexchange.com", "Stack Exchange discussion"),
    ("stackoverflow.com", "Stack Overflow discussion"),
    ("careervillage.org", "CareerVillage Q&A"),
    ("indeed.com", "Indeed career article"),
    ("medium.com", "Medium article"),
    ("gitconnected.com", "Blog article"),
]


def infer_source_type(url):
    """Guess the source type (Reddit, Medium, blog, ...) from the URL."""
    if not url:
        return "Unknown"
    lowered = url.lower()
    for domain, source_type in SOURCE_TYPE_BY_DOMAIN:
        if domain in lowered:
            return source_type
    return "Blog/Article"


def load_one_document(file_path):
    """Read one .txt file and return a consistent dictionary record.

    The body text is kept RAW (no cleaning). Only the header block is removed,
    because that block is metadata, not document content.
    """
    raw_text = file_path.read_text(encoding="utf-8", errors="ignore")

    # Find the header block (if any) and read title + url from it.
    header_match = HEADER_BLOCK_RE.search(raw_text)
    header_text = header_match.group(0) if header_match else ""

    title_match = TITLE_RE.search(header_text)
    url_match = URL_RE.search(header_text)

    title = title_match.group(1).strip() if title_match else file_path.stem
    url = url_match.group(1).strip() if url_match else ""

    # Remove ONLY the header block; leave the rest of the body untouched/raw.
    body_text = HEADER_BLOCK_RE.sub("", raw_text, count=1)

    return {
        "doc_id": file_path.stem,
        "source_filename": file_path.name,
        "source_path": str(file_path),
        "title": title,
        "url": url,
        "source_type": infer_source_type(url),
        "char_count": len(body_text),
        "raw_text": body_text,
    }


def load_all_documents():
    """Load every .txt file in DOCUMENTS_DIR into a list of records."""
    txt_files = sorted(DOCUMENTS_DIR.glob("*.txt"))
    if not txt_files:
        raise SystemExit(f"No .txt files found in '{DOCUMENTS_DIR}/'. "
                         f"Are you running this from the project root?")

    return [load_one_document(path) for path in txt_files]


def main():
    print(f"Loading documents from '{DOCUMENTS_DIR}/' ...")
    documents = load_all_documents()

    # Save the raw snapshot (indent=2 keeps it human-readable).
    OUTPUT_FILE.write_text(
        json.dumps(documents, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("\n" + "=" * 60)
    print("RAW DOCUMENT LOAD SUMMARY")
    print("=" * 60)
    print(f"Documents loaded : {len(documents)}")
    print(f"Saved to         : {OUTPUT_FILE}")
    print("-" * 60)
    for doc in documents:
        print(f"  {doc['source_filename']:35s} "
              f"{doc['char_count']:>7,d} chars  [{doc['source_type']}]")


if __name__ == "__main__":
    main()
