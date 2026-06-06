"""
ingest_and_chunk.py
===================

The CHUNKING stage of "The Unofficial CS Career Guide" RAG pipeline.

It reads the already-cleaned documents (cleaned_documents.json) and splits each
one into overlapping, token-sized chunks, then saves them to chunks.json with
full metadata so later stages can trace every chunk back to its source.

Pipeline position:
    load_documents.py  -> raw_documents.json
    clean_documents.py -> cleaned_documents.json
    ingest_and_chunk.py-> chunks.json        <-- you are here

Chunking strategy (from planning.md):
    - Chunk size : 250 tokens
    - Overlap    : 50 tokens
    These numbers were lowered from an earlier 500/75 so each chunk fits inside
    the 256-token input limit of the embedding model (all-MiniLM-L6-v2); see
    planning.md for the full reasoning.

A NOTE ON "TOKENS":
    A real tokenizer (like the one inside all-MiniLM-L6-v2) splits text into
    sub-word pieces. To keep this stage simple and dependency-free, we approximate
    one token as one whitespace-separated word. This is the common convention for
    student RAG projects and is close enough for chunking. If you later want exact
    token counts, swap count_tokens()/split_into_tokens() for the model's tokenizer.
"""

import json
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration  (matches the Chunking Strategy section in planning.md)
# ---------------------------------------------------------------------------

INPUT_FILE = Path("cleaned_documents.json")  # produced by clean_documents.py
OUTPUT_FILE = Path("chunks.json")            # where the finished chunks are written

CHUNK_SIZE = 250    # target tokens per chunk
CHUNK_OVERLAP = 50  # tokens that each chunk shares with the previous one


# ---------------------------------------------------------------------------
# Token-based chunking
# ---------------------------------------------------------------------------

def split_into_tokens(text):
    """Split text into 'tokens' (whitespace-separated words). See note at top."""
    return text.split()


def count_tokens(text):
    """Count approximate tokens in a piece of text."""
    return len(split_into_tokens(text))


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Split text into overlapping chunks of ~chunk_size tokens.

    Uses a sliding window: each new window starts `chunk_size - overlap`
    tokens after the previous one, so consecutive chunks share `overlap` tokens.
    Returns a list of chunk strings.
    """
    tokens = split_into_tokens(text)
    if not tokens:
        return []

    step = chunk_size - overlap  # how far the window moves each time
    chunks = []
    start = 0

    while start < len(tokens):
        window = tokens[start:start + chunk_size]
        chunks.append(" ".join(window))

        # If this window already reached the end, we're done.
        if start + chunk_size >= len(tokens):
            break
        start += step

    return chunks


# ---------------------------------------------------------------------------
# Main pipeline: read cleaned docs -> chunk -> save
# ---------------------------------------------------------------------------

def build_chunks(documents):
    """Chunk every cleaned document and return (chunks, doc_count)."""
    all_chunks = []
    documents_chunked = 0

    for doc in documents:
        cleaned_text = doc["cleaned_text"]

        # Skip any document that is empty after cleaning (nothing to chunk).
        if not cleaned_text.strip():
            print(f"  (skipped '{doc['source_filename']}': no content)")
            continue

        documents_chunked += 1
        pieces = chunk_text(cleaned_text)

        for index, piece in enumerate(pieces):
            all_chunks.append({
                "chunk_id": f"{doc['doc_id']}_chunk_{index}",
                "source_filename": doc["source_filename"],
                "source_path": doc["source_path"],
                "title": doc["title"],
                "url": doc["url"],
                "source_type": doc["source_type"],
                "chunk_index": index,
                "char_count": len(piece),
                "token_count": count_tokens(piece),
                "text": piece,
            })

    return all_chunks, documents_chunked


def print_summary(chunks, documents_chunked):
    """Print summary statistics and a few sample chunks."""
    total_chunks = len(chunks)
    token_counts = [c["token_count"] for c in chunks]
    avg_tokens = sum(token_counts) / total_chunks if total_chunks else 0

    print("\n" + "=" * 60)
    print("CHUNKING SUMMARY")
    print("=" * 60)
    print(f"Documents chunked    : {documents_chunked}")
    print(f"Chunks created       : {total_chunks}")
    print(f"Chunk size / overlap : {CHUNK_SIZE} / {CHUNK_OVERLAP} tokens")
    print(f"Average chunk size   : {avg_tokens:.1f} tokens")
    if token_counts:
        print(f"Smallest / largest   : {min(token_counts)} / {max(token_counts)} tokens")
    print(f"Saved to             : {OUTPUT_FILE}")

    # Show a few sample chunks so you can eyeball the chunking.
    print("\n" + "-" * 60)
    print("SAMPLE CHUNKS (first ~250 characters each)")
    print("-" * 60)
    for sample in chunks[:3]:
        preview = sample["text"][:250].replace("\n", " ")
        print(f"\n[{sample['chunk_id']}]  from: {sample['title']}")
        print(f"  tokens={sample['token_count']}  chars={sample['char_count']}")
        print(f"  {preview}...")


def main():
    if not INPUT_FILE.exists():
        raise SystemExit(f"'{INPUT_FILE}' not found. Run load_documents.py "
                         f"then clean_documents.py first.")

    print(f"Reading cleaned documents from '{INPUT_FILE}' ...")
    documents = json.loads(INPUT_FILE.read_text(encoding="utf-8"))

    chunks, documents_chunked = build_chunks(documents)

    # Save all chunks to JSON (indent=2 keeps it human-readable).
    OUTPUT_FILE.write_text(
        json.dumps(chunks, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print_summary(chunks, documents_chunked)


if __name__ == "__main__":
    main()
