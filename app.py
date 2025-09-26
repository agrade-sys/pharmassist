import gradio as gr
from agents.drug_profile_agent import render_tab as drug_tab
from agents.outreach_agent import render_tab as outreach_tab
from agents.regulatory_agent import render_tab as regulatory_tab
from agents.trial_agent import render_tab as trial_tab
from agents.ops_team_agent import render_tab as ops_tab
from agents.sidekick_agent import render_tab as sidekick_tab
from agents.creator_agent import render_tab as creator_tab

with gr.Blocks(title="Pharmassist: Drug Launch Assistant") as demo:
    with gr.Tab("Drug Profile"): drug_tab()
    with gr.Tab("Doctor Outreach"): outreach_tab()
    with gr.Tab("Regulatory Brief"): regulatory_tab()
    with gr.Tab("Trials"): trial_tab()
    with gr.Tab("Ops Team"): ops_tab()
    with gr.Tab("Sidekick"): sidekick_tab()
    with gr.Tab("Flow Creator"): creator_tab()

demo.launch(server_name="0.0.0.0", server_port=7860)
