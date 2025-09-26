import json
import gradio as gr

def load_drug_profile(file):
    if file is None: return {"error": "upload drug_profile.json"}
    data = json.load(open(file.name, "r", encoding="utf-8"))
    fields = ["name","indication","stage","target_market"]
    return {k: data.get(k, "") for k in fields}

def render_tab():
    uploader = gr.File(label="Upload drug_profile.json")
    out = gr.JSON(label="Drug Profile")
    uploader.change(load_drug_profile, inputs=uploader, outputs=out)
