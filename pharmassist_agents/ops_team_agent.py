import os
import json
import yaml
import gradio as gr
from pathlib import Path
from crewai import Agent, Task, Crew
from dotenv import load_dotenv
from .ops_team_tools import read_trials_data, read_drug_profile, read_kol_database

load_dotenv()

# Get config directory
config_dir = Path(__file__).parent / "ops_team_config"

def load_yaml(filename):
    """Load YAML configuration file"""
    with open(config_dir / filename, 'r') as f:
        return yaml.safe_load(f)

# Load configuration
agents_config = load_yaml("agents.yaml")
tasks_config = load_yaml("tasks.yaml")

def create_ops_crew():
    """Create and return the Ops Team crew"""
    # Create agents from config
    agents = {}
    for agent_name, agent_config in agents_config.items():
        # Assign tools based on agent role
        tools = []
        if "clinical" in agent_name.lower():
            tools = [read_trials_data, read_drug_profile]
        elif "regulatory" in agent_name.lower():
            tools = [read_drug_profile]
        elif "manufacturing" in agent_name.lower():
            tools = [read_drug_profile]
        elif "commercial" in agent_name.lower():
            tools = [read_kol_database, read_drug_profile]
        elif "ops_manager" in agent_name.lower():
            tools = [read_trials_data, read_drug_profile, read_kol_database]
        
        agents[agent_name] = Agent(
            role=agent_config["role"],
            goal=agent_config["goal"],
            backstory=agent_config["backstory"],
            tools=tools,
            verbose=True,
            allow_delegation=False
        )
    
    # Create tasks from config
    tasks = []
    task_order = [
        "analyze_trial_sites_task",
        "assess_regulatory_compliance_task",
        "evaluate_manufacturing_capacity_task",
        "develop_kol_strategy_task",
        "synthesize_operational_readiness_task"
    ]
    
    for task_name in task_order:
        task_config = tasks_config[task_name]
        agent_name = task_config["agent"]
        tasks.append(
            Task(
                description=task_config["description"],
                expected_output=task_config["expected_output"],
                agent=agents[agent_name]
            )
        )
    
    # Create crew
    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        verbose=True
    )
    return crew

def render_tab():
    """Render the Ops Team tab in Gradio"""
    with gr.Group():
        gr.Markdown("""
        ## 🏥 Ops Team Agent - Phase III Readiness Assessment
        
        **CrewAI Pattern (Week 3)**: Multi-agent role-based collaboration
        
        This crew assesses CardioRelief's readiness for Phase III across four domains:
        - **Clinical Ops**: Trial data analysis, site performance, enrollment strategy
        - **Regulatory Ops**: CMC readiness, compliance status, submission timeline
        - **Manufacturing Ops**: Production capacity, supply chain constraints
        - **Commercial Ops**: KOL strategy, market entry plan
        - **Ops Manager**: Synthesizes all inputs for Phase III go/no-go decision
        """)
        
        with gr.Row():
            assess_button = gr.Button("🚀 Assess Phase III Readiness", size="lg")
        
        output = gr.Textbox(
            label="Operational Readiness Report",
            lines=20,
            interactive=False,
            placeholder="Click 'Assess Phase III Readiness' to generate report..."
        )
        
        def assess_readiness():
            """Execute crew and return report"""
            try:
                crew = create_ops_crew()
                result = crew.kickoff()
                return str(result)
            except Exception as e:
                return f"❌ Error: {str(e)}"
        
        assess_button.click(
            fn=assess_readiness,
            outputs=output
        )