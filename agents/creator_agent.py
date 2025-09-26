import gradio as gr
import os, pathlib, yaml

CONFIG_DIR = pathlib.Path("config/agents")
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

def create_flow(name, goal, tools):
    if not name: return "name required"
    cfg = {"name": name, "goal": goal, "tools": [t.strip() for t in tools.split(",") if t.strip()]}
    path = CONFIG_DIR / f"{name.lower().replace(' ','_')}.yaml"
    with open(path, "w", encoding="utf-8") as f: yaml.safe_dump(cfg, f)
    return f"Created {path}"

def render_tab():
    with gr.Row():
        name = gr.Textbox(label="Agent name")
        goal = gr.Textbox(label="Goal")
    tools = gr.Textbox(label="Tools (comma-separated)", value="files,datastore,http")
    out = gr.Textbox(label="Result", interactive=False)
    btn = gr.Button("Create Flow")
    btn.click(create_flow, [name, goal, tools], out)
