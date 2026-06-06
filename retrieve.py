"""
retrieve.py
===========

The RETRIEVAL stage of "The Unofficial CS Career Guide".

Given a natural-language question, it embeds the question with the SAME model
used for the chunks (all-MiniLM-L6-v2), then asks ChromaDB for the top-k most
similar chunks. Top-k defaults to 5, matching planning.md and the architecture
diagram ("Retrieval — Similarity Search — Top 5 Chunks").

Use it two ways:
    - As a function:   from retrieve import retrieve;  retrieve("how do I prep for interviews?")
    - From the terminal:  python3 retrieve.py "how do I prep for interviews?"

The next stage (generation) will feed these retrieved chunks to Groq as context.
"""

import sys

from embed_and_store import (
    COLLECTION_NAME,
    get_client,
    load_model,
    embed_texts,
)

TOP_K = 5  # how many chunks to retrieve per query (matches the spec)
PREVIEW_CHARS = 500  # how many characters of each chunk to print when run from the CLI

# Load the model and open the collection once at import time so repeated
# retrieve() calls don't reload the model or reconnect every time.
_model = None
_collection = None


def _get_model():
    """Lazily load (and cache) the embedding model."""
    global _model
    if _model is None:
        _model = load_model()
    return _model


def _get_collection():
    """Lazily open (and cache) the ChromaDB collection."""
    global _collection
    if _collection is None:
        client = get_client()
        # get_collection opens the existing collection that embed_and_store.py
        # built. It raises if the collection doesn't exist yet.
        try:
            _collection = client.get_collection(COLLECTION_NAME)
        except Exception:
            raise SystemExit(
                f"Collection '{COLLECTION_NAME}' not found. "
                f"Run embed_and_store.py first to build the vector store."
            )
    return _collection


def retrieve(query, k=TOP_K):
    """Return the top-k most similar chunks for a query.

    Each result is a dict with the chunk text, its source metadata, and a
    similarity score in [0, 1] (higher = more relevant).
    """
    model = _get_model()
    collection = _get_collection()

    # 1) Embed the query with the same model used for the stored chunks.
    query_embedding = embed_texts(model, [query])  # list with one vector

    # 2) Ask ChromaDB for the nearest chunks. query() compares the query vector
    #    against every stored vector and returns the n_results closest ones.
    #    include= tells it which fields to return (the text, metadata, and the
    #    cosine distance). Results come back as lists-of-lists (one inner list
    #    per query); we sent one query, so we read index [0].
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    # 3) Repackage into a clean list. With cosine space, distance = 1 - cosine
    #    similarity, so similarity = 1 - distance.
    retrieved = []
    for text, meta, distance in zip(documents, metadatas, distances):
        retrieved.append({
            "text": text,
            "title": meta.get("title", ""),
            "url": meta.get("url", ""),
            "source_type": meta.get("source_type", ""),
            "source_filename": meta.get("source_filename", ""),
            "chunk_index": meta.get("chunk_index"),
            "similarity": round(1 - distance, 4),
        })
    return retrieved


def main():
    # Read the query from the command line, or fall back to a demo question.
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = "How should I prepare for a technical interview?"

    print(f"Query: {query}\n")
    results = retrieve(query)

    print("=" * 70)
    print(f"TOP {len(results)} RETRIEVED CHUNKS")
    print("=" * 70)
    for rank, item in enumerate(results, start=1):
        text = item["text"].replace("\n", " ")
        preview = text[:PREVIEW_CHARS]
        ellipsis = "..." if len(text) > PREVIEW_CHARS else ""
        distance = round(1 - item["similarity"], 4)
        print(f"\n#{rank}  similarity={item['similarity']}  distance={distance}  "
              f"[{item['source_type']}] {item['source_filename']} (chunk {item['chunk_index']})")
        print(f"    title: {item['title']}")
        print(f"    {preview}{ellipsis}")


if __name__ == "__main__":
    main()
