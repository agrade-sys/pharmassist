import gradio as gr

def generate_brief():
    # placeholder: later replace with CrewAI+LangGraph+MCP
    brief = (
        "# Regulatory Brief (Mock)\n"
        "- Pathway: Conditional marketing authorisation (EU)\n"
        "- Key docs: Module 2 summaries, risk plan\n"
        "- Timeline: 6–12 months (mock)\n"
    )
    return brief

def render_tab():
    btn = gr.Button("Generate Regulatory Brief")
    out = gr.Markdown()
    btn.click(generate_brief, None, out)
