"""
app.py
======

The INTERFACE stage of "The Unofficial CS Career Guide" — a Gradio web app
that ties the whole RAG pipeline together for an end user.

Flow when a user asks a question:
    question -> retrieve.py (top-k chunks) -> generate.py (Groq, grounded)
             -> answer (with [n] citations) + source list shown in the browser

Run it:
    python3 app.py
Then open the local URL it prints (e.g. http://127.0.0.1:7860).

Prerequisites (run once, in order):
    python3 load_documents.py
    python3 clean_documents.py
    python3 ingest_and_chunk.py
    python3 embed_and_store.py     # builds the vector store
And a GROQ_API_KEY in your .env file.
"""

import gradio as gr

from generate import generate_answer
from retrieve import TOP_K

# Example questions (your planning.md evaluation queries) to seed the UI.
EXAMPLE_QUESTIONS = [
    "What practical skills does college not teach CS students?",
    "How experienced are students before their first internship?",
    "What personal projects are good for a CS resume?",
    "How do I prepare for a technical interview?",
    "How should a beginner start their first personal project?",
]


def answer_question(question, k):
    """Gradio callback: question -> (answer markdown, sources markdown)."""
    question = (question or "").strip()
    if not question:
        return "Please enter a question.", ""

    result = generate_answer(question, k=int(k))
    return result["answer"], result["sources_markdown"]


def build_ui():
    """Assemble the Gradio Blocks interface (the 'skeleton')."""
    with gr.Blocks(title="The Unofficial CS Career Guide") as demo:
        # --- Header ---
        gr.Markdown(
            "# The Unofficial CS Career Guide\n"
            "Ask about CS internships, interviews, resumes, personal projects, "
            "and the practical skills college doesn't teach. Answers are grounded "
            "**only** in the collected sources, with citations."
        )

        # --- Inputs ---
        with gr.Row():
            question_box = gr.Textbox(
                label="Your question",
                placeholder="e.g. How do I prepare for a technical interview?",
                lines=2,
                scale=4,
            )
            k_slider = gr.Slider(
                minimum=1, maximum=10, value=TOP_K, step=1,
                label="Chunks to retrieve (top-k)", scale=1,
            )
        ask_button = gr.Button("Ask", variant="primary")

        gr.Examples(examples=EXAMPLE_QUESTIONS, inputs=question_box)

        # --- Outputs ---
        answer_box = gr.Markdown(label="Answer")
        sources_box = gr.Markdown(label="Sources")

        # --- Wiring: button click and Enter both trigger the callback ---
        ask_button.click(
            fn=answer_question,
            inputs=[question_box, k_slider],
            outputs=[answer_box, sources_box],
        )
        question_box.submit(
            fn=answer_question,
            inputs=[question_box, k_slider],
            outputs=[answer_box, sources_box],
        )

    return demo


if __name__ == "__main__":
    build_ui().launch()
