import csv, io
import gradio as gr

def analyze_trials(csv_file):
    if csv_file is None: return "upload trials.csv"
    rows = list(csv.DictReader(io.StringIO(csv_file.decode())))
    n = len(rows)
    complete = sum(float(r.get("completion_pct","0") or 0) for r in rows)/max(n,1)
    plan = "Continue Phase II with safety monitoring." if complete >= 50 else "Adjust enrollment strategy."
    md = f"**Trials:** {n} records\n**Avg completion:** {complete:.1f}%\n**Plan:** {plan}"
    return md

def render_tab():
    uploader = gr.File(label="Upload trials.csv", file_types=[".csv"])
    out = gr.Markdown()
    uploader.upload(fn=lambda f: analyze_trials(f.read()), inputs=uploader, outputs=out)
