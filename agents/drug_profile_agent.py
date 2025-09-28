import os
import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader  

load_dotenv()

client = OpenAI()

def parse_pdf(file):
    if file is None:
        return {"error": "❌ Please upload a PDF file"}, ""
    
    try:
        reader = PdfReader(file.name)
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        
        # Clean metadata display
        profile = {
            "📄 Filename": os.path.basename(file.name),
            "📑 Pages": len(reader.pages),
            "📝 Text Length": f"{len(text):,} characters",
            "🔍 Preview": text[:200] + "..." if len(text) > 200 else text,
            "✅ Status": "Successfully extracted"
        }
        return profile, text
        
    except Exception as e:
        error_profile = {
            "❌ Error": f"Failed to process PDF: {str(e)}",
            "📄 Filename": os.path.basename(file.name) if file else "Unknown"
        }
        return error_profile, ""

def generate_candidates(text, progress=gr.Progress()):
    if not text or text.strip() == "":
        return "Please upload a PDF first", []
    
    # Speed optimization: Truncate text
    if len(text) > 3000:
        text = text[:3000] + "\n\n[Text truncated for processing speed]"
    
    progress(0, desc="🔄 Starting strategy generation...")
    
    question = "Based on this drug profile, what are the best next development strategies? Be concise."
    candidates = []
    
    for i in range(3):
        progress((i)/3, desc=f"⏳ Generating Strategy {i+1}/3...")
        try:
            resp = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),  # Faster model
                messages=[
                    {"role":"system","content":"You are an expert pharma strategist. Provide concise, actionable strategies in 2-3 paragraphs maximum."},
                    {"role":"user","content":f"{question}\n\n{text}\n\nStrategy {i+1}:"}
                ],
                max_tokens=300,  # Shorter responses = faster
                timeout=20       # Shorter timeout
            )
            candidate = resp.choices[0].message.content.strip()
            candidates.append(candidate)
            
        except Exception as e:
            error_msg = f"❌ Error generating strategy {i+1}: {str(e)}"
            candidates.append(error_msg)
            print(error_msg)
    
    progress(1.0, desc="✅ Complete!")
    
    # Format final output with clean styling
    formatted_output = "# 🎯 Development Strategy Candidates\n\n"
    for i, candidate in enumerate(candidates, 1):
        formatted_output += f"## 📋 Strategy {i}\n\n{candidate}\n\n---\n\n"
    
    return formatted_output, candidates

def judge_candidates(candidates, progress=gr.Progress()):
    if not candidates or len(candidates) == 0:
        return "❌ No candidates to judge. Please generate strategies first."
    
    progress(0, desc="🔄 Starting evaluation...")
    
    judge_prompt = (
        "Rank these drug development strategies for feasibility and regulatory success. Provide a clear ranking with brief explanations:\n\n" +
        "\n\n".join([f"**Strategy {i+1}:** {c}" for i,c in enumerate(candidates)])
    )
    
    progress(0.5, desc="⚖️ Analyzing strategies...")
    
    try:
        resp = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role":"system","content":"You are a strict pharmaceutical strategy evaluator. Provide clear rankings with reasoning."},
                {"role":"user","content":judge_prompt}
            ],
            max_tokens=500,
            timeout=30
        )
        
        progress(1.0, desc="✅ Evaluation complete!")
        
        # Format the ranking nicely
        ranking_result = f"# 🏆 Strategy Evaluation & Ranking\n\n{resp.choices[0].message.content.strip()}"
        return ranking_result
        
    except Exception as e:
        error_msg = f"❌ Error during evaluation: {str(e)}"
        print(error_msg)
        return error_msg

def render_tab():
    with gr.Column():
        gr.Markdown("Upload a **drug_profile.pdf** → extract text → generate strategies → rank them.")
        uploader = gr.File(label="Upload PDF", file_types=[".pdf"])
        profile_out = gr.JSON(label="📋 Extracted Metadata")
        candidates_out = gr.Markdown(label="🎯 Candidate Strategies")
        final_out = gr.Markdown(label="🏆 Ranked Best Plan")

        state_text = gr.State()
        state_candidates = gr.State()

        uploader.change(parse_pdf, inputs=uploader, outputs=[profile_out, state_text])
        gen_btn = gr.Button("🚀 Step 1: Generate Candidate Strategies", variant="primary")
        judge_btn = gr.Button("⚖️ Step 2: Judge and Rank", variant="secondary")

        gen_btn.click(generate_candidates, inputs=state_text, outputs=[candidates_out, state_candidates])
        judge_btn.click(judge_candidates, inputs=state_candidates, outputs=final_out)
