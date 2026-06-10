"""Gradio interface for the ASU CS unofficial guide."""

from __future__ import annotations

import gradio as gr

from query import ask


def handle_query(question: str) -> tuple[str, str]:
    try:
        result = ask(question)
    except Exception as exc:  # Keep setup/runtime errors visible in the UI.
        return f"Error: {exc}", ""

    sources = "\n\n".join(result["sources"])
    if not sources:
        sources = "No sources returned."
    return result["answer"], sources


with gr.Blocks(title="ASU CS Unofficial Guide") as demo:
    gr.Markdown("# The Unofficial Guide: ASU CS Course Planning")
    question = gr.Textbox(
        label="Your question",
        placeholder="Ask about ASU CS course planning, workload, advising, or tutoring.",
        lines=2,
    )
    ask_button = gr.Button("Ask", variant="primary")
    answer = gr.Textbox(label="Answer", lines=10)
    sources = gr.Textbox(label="Retrieved from", lines=8)

    ask_button.click(handle_query, inputs=question, outputs=[answer, sources])
    question.submit(handle_query, inputs=question, outputs=[answer, sources])


if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860, share=False)
