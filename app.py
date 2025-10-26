import gradio as gr
from pharmassist_agents.drug_profile_agent import render_tab as drug_tab
from pharmassist_agents.regulatory_agent import render_tab as regulatory_tab
# from pharmassist_agents.outreach_agent import render_tab as outreach_tab
from pharmassist_agents.trial_agent import render_tab as trial_tab
from pharmassist_agents.ops_team_agent import render_tab as ops_tab
from pharmassist_agents.creator_agent import render_tab as creator_tab

with gr.Blocks(title="Pharmassist: Drug Launch Assistant") as demo:
    gr.Markdown("""
    # 🏥 Pharmassist: Drug Launch Assistant
    
    **Agentic AI for Pharmaceutical Development**
    
    Demonstrating concepts from [The Complete Agentic AI Engineering Course (2025)] by Ed Donner
    
    ### Implemented Agents:
    - **Drug Profile** (Week 1) - Conversational AI with tool calling
    - **Regulatory Brief** (Week 2) - Multi-agent collaboration with OpenAI SDK
    
    ### Planned Agents:
    - Doctor Outreach, Clinical Trials, Ops Team, Flow Creator
    """)
    
    with gr.Tab("Drug Profile"): 
        drug_tab()
    
    with gr.Tab("Regulatory Brief"): 
        regulatory_tab()
    
    with gr.Tab("Clinical Trials"): 
        trial_tab()
    
   # with gr.Tab("Doctor Outreach"): 
   #     outreach_tab()
    
    with gr.Tab("Ops Team"): 
        ops_tab()
    
    with gr.Tab("Flow Creator"): 
        creator_tab()

demo.launch(server_port=7860)