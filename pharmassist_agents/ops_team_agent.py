import gradio as gr

def simulate_ops():
    # placeholder: later replace with 4-agent simulation
    return (
        "**Clinical:** proceed with interim analysis.\n"
        "**Regulatory:** prepare Q&A package.\n"
        "**Marketing:** draft HCP education deck.\n"
        "**Commercial:** refine target center list."
    )

def render_tab():
    btn = gr.Button("Run 4-Agent Ops Simulation")
    out = gr.Markdown()
    btn.click(simulate_ops, None, out)
