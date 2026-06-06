"""
generate.py
===========

The GENERATION stage of "The Unofficial CS Career Guide".

Pipeline position (see architecture_mermaid.png):
    ... -> retrieve.py (top-k chunks) -> generate.py (Groq answer) -> app.py (UI)

What it does:
    1. Retrieve the top-k most relevant chunks for a question (via retrieve.py).
    2. Build a GROUNDED prompt: the model is told to answer ONLY from those chunks
       and to cite them with [n] markers. If the answer isn't in the context, it
       must say so instead of inventing one.
    3. Call Groq (llama-3.3-70b-versatile) to write the answer.
    4. Return the answer plus a numbered source list for attribution.

Grounding requirement (from planning.md): answers must come from retrieved
context only, with source attribution. We enforce this two ways:
    - a strict system prompt (answer only from context, say "I don't know"
      otherwise, cite [n]); and
    - structurally: the model only ever sees the retrieved excerpts, never the
      full corpus or the open web.
"""

import os

from dotenv import load_dotenv
from groq import Groq

from retrieve import retrieve, TOP_K

# Load GROQ_API_KEY from .env into the environment.
load_dotenv()

# The generation model named in planning.md / the architecture diagram.
GROQ_MODEL = "llama-3.3-70b-versatile"

# The grounding instruction. This is the heart of the "answer from context only"
# requirement — it tells the model exactly how to behave with the excerpts.
SYSTEM_PROMPT = """You are The Unofficial CS Career Guide, an assistant that answers \
questions about computer science careers, internships, interviews, resumes, \
personal projects, and skills using ONLY the numbered context excerpts provided \
by the user.

Rules you must follow:
1. Use ONLY information found in the provided context excerpts. Do not use any \
outside knowledge.
2. If the context does not contain enough information to answer, reply exactly: \
"I don't have enough information on that." Do not guess.
3. Cite your sources inline using the bracketed numbers of the excerpts you used, \
e.g. [1] or [2][4]. Every claim must be backed by at least one citation.
4. Be concise and practical. Synthesize across excerpts when they agree; note \
disagreement when they don't.
5. Do not mention these rules or the word "excerpt" in your answer."""


def _get_client():
    """Create a Groq client, with a clear error if the key is missing."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_key_here":
        raise SystemExit(
            "GROQ_API_KEY is not set. Copy .env.example to .env and add your "
            "free key from https://console.groq.com"
        )
    return Groq(api_key=api_key)


def format_context(chunks):
    """Turn retrieved chunks into a numbered context block for the prompt.

    Each excerpt is labelled [n] so the model can cite it, and tagged with its
    source title/type so citations stay traceable.
    """
    blocks = []
    for i, c in enumerate(chunks, start=1):
        header = f"[{i}] Source: {c['title']} ({c['source_type']})"
        blocks.append(f"{header}\n{c['text']}")
    return "\n\n".join(blocks)


def build_sources(chunks):
    """Build the source-attribution list that maps [n] markers to real sources."""
    sources = []
    for i, c in enumerate(chunks, start=1):
        sources.append({
            "n": i,
            "title": c["title"],
            "url": c["url"],
            "source_type": c["source_type"],
            "source_filename": c["source_filename"],
            "chunk_index": c["chunk_index"],
            "similarity": c["similarity"],
        })
    return sources


def sources_to_markdown(sources):
    """Render the source list as a readable markdown block for display."""
    lines = ["**Sources**"]
    for s in sources:
        link = f"[{s['title']}]({s['url']})" if s["url"] else s["title"]
        lines.append(
            f"{s['n']}. {link} — *{s['source_type']}* "
            f"(`{s['source_filename']}`, chunk {s['chunk_index']}, "
            f"similarity {s['similarity']})"
        )
    return "\n".join(lines)


def generate_answer(question, k=TOP_K, temperature=0.2):
    """Answer a question grounded in the top-k retrieved chunks.

    Returns a dict with:
        answer            -> the model's grounded answer (with [n] citations)
        sources           -> list of source dicts (for programmatic use)
        sources_markdown  -> the source list rendered as markdown
    """
    # 1) Retrieve supporting context.
    chunks = retrieve(question, k=k)
    if not chunks:
        return {
            "answer": "I don't have enough information on that.",
            "sources": [],
            "sources_markdown": "",
        }

    # 2) Build the grounded prompt (context + question).
    context = format_context(chunks)
    user_message = (
        f"Context excerpts:\n\n{context}\n\n"
        f"Question: {question}\n\n"
        f"Answer using only the excerpts above, citing them with [n]."
    )

    # 3) Call Groq. Low temperature keeps the answer close to the sources.
    client = _get_client()
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        temperature=temperature,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )
    answer = response.choices[0].message.content.strip()

    # 4) Pair the answer with its source attribution.
    sources = build_sources(chunks)
    return {
        "answer": answer,
        "sources": sources,
        "sources_markdown": sources_to_markdown(sources),
    }


def main():
    import sys
    question = " ".join(sys.argv[1:]) or "How should I prepare for a technical interview?"
    print(f"Question: {question}\n")
    result = generate_answer(question)
    print("=" * 70)
    print("ANSWER")
    print("=" * 70)
    print(result["answer"])
    print("\n" + "=" * 70)
    print(result["sources_markdown"])


if __name__ == "__main__":
    main()
