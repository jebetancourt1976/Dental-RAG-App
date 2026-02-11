import gradio as gr
from app.rag import rag_chain

def ask_policy(question):
    return rag_chain.invoke(question)

def launch_ui():
    demo = gr.Interface(
        fn=ask_policy,
        inputs=gr.Textbox(label="Ask about dental coverage"),
        outputs=gr.Textbox(label="Answer"),
        title="🦷 Dental Coverage Assistant",
        description="Answers are based only on the official dental policy."
    )
    demo.launch(server_name="0.0.0.0", server_port=7860)

if __name__ == "__main__":
    launch_ui()