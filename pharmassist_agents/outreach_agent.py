import gradio as gr
import os
import csv
import io
from dotenv import load_dotenv
from openai import OpenAI
from openai.lib._agents import Agent, Runner
from pydantic import BaseModel, Field
from typing import Dict
import asyncio

load_dotenv(override=True)

# Structured output model for emails (Lab 3 concept)
class EmailOutput(BaseModel):
    subject: str = Field(description="Compelling email subject line")
    body: str = Field(description="Complete email body text")
    tone: str = Field(description="Tone used: formal, scientific, or engaging")

    # Tool functions for logging (Lab 2 @function_tool pattern)
@function_tool
def record_doctor_outreach(doctor_name: str, specialty: str, email_tone: str) -> Dict[str, str]:
    """Record that outreach was generated for a specific doctor"""
    print(f"📧 Outreach Generated:")
    print(f"   Doctor: Dr. {doctor_name}")
    print(f"   Specialty: {specialty}")
    print(f"   Tone: {email_tone}")
    return {"status": "recorded"}

@function_tool
def flag_for_followup(doctor_name: str, reason: str) -> Dict[str, str]:
    """Flag a doctor for manual follow-up"""
    print(f"🚩 Flagged for Follow-up:")
    print(f"   Doctor: Dr. {doctor_name}")
    print(f"   Reason: {reason}")
    return {"status": "flagged"}

    # Three outreach agents with different styles (Lab 2 pattern)
formal_instructions = """You are a formal, professional medical outreach specialist.
You write respectful, clinical emails to physicians about new pharmaceutical developments.
Your tone is professional, evidence-based, and appropriate for peer-to-peer medical communication.
Focus on clinical efficacy, safety data, and regulatory status."""

scientific_instructions = """You are a scientific medical writer specializing in physician outreach.
You write data-driven, research-focused emails emphasizing clinical trial results and mechanisms of action.
Your tone is academic and precise, citing specific endpoints and statistical significance.
Appeal to the physician's scientific curiosity and evidence-based practice."""

engaging_instructions = """You are an engaging, relationship-focused medical liaison.
You write warm, conversational emails that build rapport while remaining professional.
Your tone is friendly and enthusiastic, highlighting practical patient benefits.
Make the email feel personal and relevant to the physician's daily practice."""

# Create the three agents
formal_agent = Agent(
    name="Formal Outreach Agent",
    instructions=formal_instructions,
    model="gpt-4o-mini",
    output_type=EmailOutput
)

scientific_agent = Agent(
    name="Scientific Outreach Agent", 
    instructions=scientific_instructions,
    model="gpt-4o-mini",
    output_type=EmailOutput
)

engaging_agent = Agent(
    name="Engaging Outreach Agent",
    instructions=engaging_instructions,
    model="gpt-4o-mini",
    output_type=EmailOutput
)
# Convert agents to tools (Lab 2 agent-as-tool pattern)
formal_tool = formal_agent.as_tool(
    tool_name="formal_outreach",
    tool_description="Generate a formal, professional medical outreach email"
)

scientific_tool = scientific_agent.as_tool(
    tool_name="scientific_outreach", 
    tool_description="Generate a scientific, research-focused outreach email"
)

engaging_tool = engaging_agent.as_tool(
    tool_name="engaging_outreach",
    tool_description="Generate an engaging, relationship-building outreach email"
)

# Manager agent that coordinates the three agents (Lab 2 orchestration pattern)
manager_instructions = """You are an Outreach Manager coordinating physician outreach campaigns.

Your workflow:
1. Use ALL THREE outreach agent tools to generate three different email approaches
2. Evaluate each email for effectiveness, appropriateness, and likelihood of response
3. Select the SINGLE best email that balances professionalism with engagement
4. Use record_doctor_outreach tool to log the outreach
5. Return the winning email

Be decisive in your choice. Consider the specialty and context when selecting."""

outreach_manager = Agent(
    name="Outreach Manager",
    instructions=manager_instructions,
    tools=[formal_tool, scientific_tool, engaging_tool, record_doctor_outreach],
    model="gpt-4o-mini"
)
# Main outreach function using async/await (Lab 2 Runner pattern)
async def generate_outreach(doctor_name: str, specialty: str) -> str:
    """Generate outreach email for a doctor using multi-agent collaboration"""
    
    message = f"Generate the best outreach email for:\nDoctor: Dr. {doctor_name}\nSpecialty: {specialty}\n\nThe email should introduce CardioRelief, our new drug for chronic heart failure."
    
    try:
        with trace("Doctor Outreach"):
            print(f"\n🔄 Generating outreach for Dr. {doctor_name} ({specialty})...")
            result = await Runner.run(outreach_manager, message)
            print(f"✅ Outreach complete!\n")
            return result.final_output
    except Exception as e:
        error_msg = f"❌ Error generating outreach: {str(e)}"
        print(error_msg)
        return error_msg

def render_tab():
    """Render the Doctor Outreach agent interface"""
    
    with gr.Column():
        gr.Markdown("""
        # 📧 Doctor Outreach Agent
        
        **Multi-Agent Email Generation System (Week 2 - Lab 2)**
        
        This agent uses **OpenAI Agents SDK** to coordinate three competing outreach agents:
        - 🎩 Formal Agent - Professional, clinical communication
        - 🔬 Scientific Agent - Research-focused, data-driven
        - 🤝 Engaging Agent - Warm, relationship-building
        
        The **Outreach Manager** evaluates all three and selects the best approach.
        
        **Demonstrates:** Multi-agent collaboration, agent-as-tool pattern, handoffs, structured outputs
        """)
        
        with gr.Row():
            doctor_name = gr.Textbox(
                label="Doctor Name",
                placeholder="e.g., Sarah Johnson",
                value="Sarah Johnson"
            )
            specialty = gr.Textbox(
                label="Specialty", 
                placeholder="e.g., Cardiology",
                value="Cardiology"
            )
        
        generate_btn = gr.Button("🚀 Generate Outreach Email", variant="primary")
        
        output = gr.Markdown(label="Generated Email")
        
        def run_outreach(name, spec):
            """Wrapper to run async function in Gradio"""
            if not name or not spec:
                return "❌ Please provide both doctor name and specialty"
            
            try:
                # Run async function in event loop
                result = asyncio.run(generate_outreach(name, spec))
                return result
            except Exception as e:
                return f"❌ Error: {str(e)}"
        
        generate_btn.click(
            fn=run_outreach,
            inputs=[doctor_name, specialty],
            outputs=output
        )
        
        gr.Markdown("""
        ---
        **Watch your terminal** for logs showing:
        - Which agents were called
        - The manager's decision process
        - Doctor outreach records
        
        **Check OpenAI traces** at: https://platform.openai.com/traces
        """)