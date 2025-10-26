import gradio as gr
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import Dict
import asyncio

load_dotenv(override=True)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Structured output model for emails (Lab 3 concept)
class EmailOutput(BaseModel):
    subject: str = Field(description="Compelling email subject line")
    body: str = Field(description="Complete email body text")
    tone: str = Field(description="Tone used: formal, scientific, or engaging")

# Tool functions for logging
def record_doctor_outreach(doctor_name: str, specialty: str, email_tone: str) -> Dict[str, str]:
    """Record that outreach was generated for a specific doctor"""
    print(f"📧 Outreach Generated:")
    print(f"   Doctor: Dr. {doctor_name}")
    print(f"   Specialty: {specialty}")
    print(f"   Tone: {email_tone}")
    return {"status": "recorded"}

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

def generate_formal_email(doctor_name: str, specialty: str) -> str:
    """Generate formal outreach email using OpenAI API"""
    prompt = f"""Generate a formal, professional outreach email for:
Doctor: Dr. {doctor_name}
Specialty: {specialty}

Introduce CardioRelief, a new drug for chronic heart failure. Focus on clinical data and efficacy.
Return as JSON with 'subject' and 'body' fields."""
    
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": formal_instructions},
            {"role": "user", "content": prompt}
        ],
        response_format=EmailOutput
    )
    return response.choices[0].message.parsed

def generate_scientific_email(doctor_name: str, specialty: str) -> str:
    """Generate scientific outreach email using OpenAI API"""
    prompt = f"""Generate a scientific, research-focused outreach email for:
Doctor: Dr. {doctor_name}
Specialty: {specialty}

Introduce CardioRelief, emphasizing trial data, LVEF improvement, and mechanisms of action.
Return as JSON with 'subject' and 'body' fields."""
    
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": scientific_instructions},
            {"role": "user", "content": prompt}
        ],
        response_format=EmailOutput
    )
    return response.choices[0].message.parsed

def generate_engaging_email(doctor_name: str, specialty: str) -> str:
    """Generate engaging outreach email using OpenAI API"""
    prompt = f"""Generate an engaging, warm outreach email for:
Doctor: Dr. {doctor_name}
Specialty: {specialty}

Introduce CardioRelief in a friendly way, focusing on patient benefits and practical value.
Return as JSON with 'subject' and 'body' fields."""
    
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": engaging_instructions},
            {"role": "user", "content": prompt}
        ],
        response_format=EmailOutput
    )
    return response.choices[0].message.parsed

def select_best_email(doctor_name: str, specialty: str, formal: EmailOutput, scientific: EmailOutput, engaging: EmailOutput) -> tuple:
    """Use OpenAI to evaluate and select the best email"""
    prompt = f"""You are an Outreach Manager evaluating three email approaches for:
Doctor: Dr. {doctor_name}
Specialty: {specialty}

Formal Email:
Subject: {formal.subject}
Body: {formal.body}

Scientific Email:
Subject: {scientific.subject}
Body: {scientific.body}

Engaging Email:
Subject: {engaging.subject}
Body: {engaging.body}

Which email is BEST for this doctor? Reply with ONLY the word: formal, scientific, or engaging"""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    
    choice = response.choices[0].message.content.strip().lower()
    
    if "formal" in choice:
        return formal, "formal"
    elif "scientific" in choice:
        return scientific, "scientific"
    else:
        return engaging, "engaging"

async def generate_outreach(doctor_name: str, specialty: str) -> str:
    """Generate outreach email using multi-agent collaboration"""
    
    print(f"\n🔄 Generating outreach for Dr. {doctor_name} ({specialty})...")
    
    try:
        # Generate all three approaches
        print("  📧 Generating formal email...")
        formal_email = generate_formal_email(doctor_name, specialty)
        
        print("  📧 Generating scientific email...")
        scientific_email = generate_scientific_email(doctor_name, specialty)
        
        print("  📧 Generating engaging email...")
        engaging_email = generate_engaging_email(doctor_name, specialty)
        
        # Manager evaluates and selects best
        print("  🤔 Manager evaluating approaches...")
        best_email, tone = select_best_email(doctor_name, specialty, formal_email, scientific_email, engaging_email)
        
        # Record the outreach
        record_doctor_outreach(doctor_name, specialty, tone)
        
        print(f"✅ Selected: {tone.upper()} approach\n")
        
        # Format output
        output = f"""## ✅ Outreach Email Generated ({tone.upper()})

**Subject:** {best_email.subject}

---

{best_email.body}

---

**Tone Used:** {best_email.tone}
"""
        return output
        
    except Exception as e:
        error_msg = f"❌ Error generating outreach: {str(e)}"
        print(error_msg)
        return error_msg

def render_tab():
    """Render the Doctor Outreach agent interface"""

    with gr.Column():
        gr.Markdown("""
        # 📧 Doctor Outreach Agent

        **Multi-Agent Email Generation System (Week 2)**

        This agent uses **OpenAI API** to coordinate three competing outreach approaches:
        - 🎩 Formal Agent - Professional, clinical communication
        - 🔬 Scientific Agent - Research-focused, data-driven
        - 🤝 Engaging Agent - Warm, relationship-building

        The **Outreach Manager** evaluates all three and selects the best approach.

        **Demonstrates:** Multi-agent pattern, structured outputs, email generation
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
        **Watch your terminal** for logs showing the three agent approaches and manager's decision.
        """)