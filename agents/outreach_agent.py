import csv, io
import gradio as gr

def draft_emails(csv_file):
    if csv_file is None: return "upload doctors.csv"
    rows = list(csv.DictReader(io.StringIO(csv_file.decode())))
    drafts = []
    for r in rows:
        drafts.append({
            "doctor": r.get("name",""),
            "specialty": r.get("specialty",""),
            "email_draft": f"Dear Dr. {r.get('name','')}, here is an educational update on our therapy for {r.get('specialty','')}."
        })
    # Return as markdown table for quick view
    md = "|Doctor|Specialty|Draft|\n|---|---|---|\n" + "\n".join(
        f"|{d['doctor']}|{d['specialty']}|{d['email_draft']}|" for d in drafts)
    return md

def render_tab():
    uploader = gr.File(label="Upload doctors.csv", file_types=[".csv"])
    out = gr.Markdown()
    uploader.upload(fn=lambda f: draft_emails(f.read()), inputs=uploader, outputs=out)
