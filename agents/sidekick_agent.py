import gradio as gr

def summarize(text):
    if not text: return "paste text or upload later"
    return "• " + " ".join(text.split()[:80]) + " …"

def render_tab():
    txt = gr.Textbox(lines=8, label="Paste text to summarize")
    out = gr.Markdown()
    btn = gr.Button("Summarize")
    btn.click(summarize, txt, out)
