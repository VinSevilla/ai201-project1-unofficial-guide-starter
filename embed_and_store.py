"""
embed_and_store.py
==================

The EMBEDDING + VECTOR STORE stage of "The Unofficial CS Career Guide".

Pipeline position (see architecture_mermaid.png):
    load_documents.py  -> raw_documents.json
    clean_documents.py -> cleaned_documents.json
    ingest_and_chunk.py-> chunks.json
    embed_and_store.py -> chroma_db/   (ChromaDB vector store)   <-- you are here
    retrieve.py        -> top-k similarity search
    (generation with Groq comes next)

What it does:
    1. Load the chunks produced by the chunking stage (chunks.json).
    2. Turn each chunk's text into a 384-dimension embedding vector using the
       all-MiniLM-L6-v2 sentence-transformers model.
    3. Store the vectors + chunk text + source metadata in a persistent ChromaDB
       collection on disk (the chroma_db/ folder), so retrieval can search them.

Re-running this script rebuilds the collection from scratch, so it's safe to run
again whenever chunks.json changes.
"""

import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

# ---------------------------------------------------------------------------
# Configuration  (shared with retrieve.py, which imports from this file)
# ---------------------------------------------------------------------------

CHUNKS_FILE = Path("chunks.json")     # input: produced by ingest_and_chunk.py
PERSIST_DIR = "chroma_db"             # folder where ChromaDB saves its data
COLLECTION_NAME = "cs_career_guide"   # name of the vector collection

# The embedding model named in planning.md / the architecture diagram.
# all-MiniLM-L6-v2 maps text to 384-dimension vectors and is small + fast on CPU.
MODEL_NAME = "all-MiniLM-L6-v2"

# Metadata keys (from chunks.json) we copy into the vector store. ChromaDB only
# accepts scalar metadata values (str / int / float / bool), which these all are.
METADATA_KEYS = [
    "source_filename", "source_path", "title", "url",
    "source_type", "chunk_index", "token_count", "char_count",
]


# ---------------------------------------------------------------------------
# Shared helpers (also used by retrieve.py)
# ---------------------------------------------------------------------------

def load_model():
    """Load the sentence-transformers embedding model."""
    return SentenceTransformer(MODEL_NAME)


def get_client():
    """Return a ChromaDB client that persists data to the PERSIST_DIR folder.

    PersistentClient writes the collection to disk so the embeddings survive
    between runs — you embed once here, then retrieve.py reads the same store.
    """
    return chromadb.PersistentClient(path=PERSIST_DIR)


def embed_texts(model, texts):
    """Turn a list of strings into a list of embedding vectors.

    normalize_embeddings=True scales each vector to length 1, which makes cosine
    similarity (what we configure the collection to use) behave consistently.
    """
    embeddings = model.encode(
        texts,
        batch_size=64,
        normalize_embeddings=True,
        show_progress_bar=True,
    )
    return embeddings.tolist()  # ChromaDB wants plain Python lists, not numpy


# ---------------------------------------------------------------------------
# Build the vector store
# ---------------------------------------------------------------------------

def main():
    if not CHUNKS_FILE.exists():
        raise SystemExit(f"'{CHUNKS_FILE}' not found. Run the ingestion pipeline "
                         f"(load -> clean -> ingest_and_chunk) first.")

    chunks = json.loads(CHUNKS_FILE.read_text(encoding="utf-8"))
    print(f"Loaded {len(chunks)} chunks from '{CHUNKS_FILE}'.")

    # 1) Load the embedding model.
    print(f"Loading embedding model '{MODEL_NAME}' ...")
    model = load_model()

    # 2) Connect to ChromaDB and start from a clean collection.
    client = get_client()
    # delete_collection removes any previous build so we don't get duplicate IDs.
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass  # nothing to delete on the first run

    # create_collection makes a fresh collection. The metadata dict sets the
    # similarity metric: "cosine" measures the angle between vectors, which is
    # the standard choice for sentence-transformer embeddings.
    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    # 3) Prepare the parallel lists ChromaDB's add() expects.
    ids = [chunk["chunk_id"] for chunk in chunks]
    documents = [chunk["text"] for chunk in chunks]
    metadatas = [{key: chunk[key] for key in METADATA_KEYS} for chunk in chunks]

    # 4) Embed every chunk's text.
    print("Embedding chunks ...")
    embeddings = embed_texts(model, documents)

    # 5) Store everything in the collection. add() inserts each record by id with
    #    its vector (embeddings), original text (documents), and metadata.
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
    )

    # collection.count() returns how many records are now stored.
    print("\n" + "=" * 60)
    print("EMBEDDING + VECTOR STORE SUMMARY")
    print("=" * 60)
    print(f"Model            : {MODEL_NAME} (384-dim vectors)")
    print(f"Vectors stored   : {collection.count()}")
    print(f"Collection       : {COLLECTION_NAME}")
    print(f"Persisted to     : {PERSIST_DIR}/")
    print("Next step        : run retrieve.py to search the store.")


if __name__ == "__main__":
    main()
