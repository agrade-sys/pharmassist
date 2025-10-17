import os
import gradio as gr
import json
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader  

load_dotenv()

client = OpenAI()


def record_strategy_decision(drug_name, chosen_strategy, rationale):
    """Record when user selects a development strategy"""
    print(f"📋 Strategy Decision for {drug_name}:")
    print(f"   Chosen: {chosen_strategy}")
    print(f"   Rationale: {rationale}")
    # Add push notification here later
    return {"recorded": "ok"}

def record_safety_concern(drug_name, concern):
    """Record safety concerns raised during discussion"""
    print(f"⚠️ Safety Concern for {drug_name}: {concern}")
    return {"recorded": "ok"}

def record_regulatory_question(question):
    """Record regulatory questions that couldn't be answered"""
    print(f"❓ Regulatory Question: {question}")
    return {"recorded": "ok"}

def analyze_drug_profile(file_path):
    """Analyze uploaded drug profile PDF"""
    print(f"📄 Analyzing drug profile: {file_path}")
    try:
        reader = PdfReader(file_path)
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        
        # Generate strategies from the PDF
        strategies = []
        for i in range(3):
            resp = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": "You are an expert pharma strategist. Provide concise, actionable strategies in 2-3 paragraphs maximum."},
                    {"role": "user", "content": f"Based on this drug profile, what are the best next development strategies?\n\n{text[:3000]}\n\nStrategy {i+1}:"}
                ],
                max_tokens=300
            )
            strategies.append(resp.choices[0].message.content.strip())
        
        # Format results
        result = "## Drug Profile Analysis\n\n"
        for i, strategy in enumerate(strategies, 1):
            result += f"### Strategy {i}\n\n{strategy}\n\n"
        
        return {"analysis": result}
    except Exception as e:
        return {"error": f"Failed to analyze PDF: {str(e)}"}

    # Tool definitions for OpenAI function calling
record_strategy_decision_json = {
    "name": "record_strategy_decision",
    "description": "Use this tool when the user decides on a development strategy for their drug",
    "parameters": {
        "type": "object",
        "properties": {
            "drug_name": {
                "type": "string",
                "description": "The name of the drug being discussed"
            },
            "chosen_strategy": {
                "type": "string",
                "description": "The strategy the user has chosen"
            },
            "rationale": {
                "type": "string",
                "description": "Why this strategy was chosen"
            }
        },
        "required": ["drug_name", "chosen_strategy"],
        "additionalProperties": False
    }
}

record_safety_concern_json = {
    "name": "record_safety_concern",
    "description": "Use this tool when safety concerns are raised about a drug",
    "parameters": {
        "type": "object",
        "properties": {
            "drug_name": {
                "type": "string",
                "description": "The drug name"
            },
            "concern": {
                "type": "string",
                "description": "The safety concern raised"
            }
        },
        "required": ["drug_name", "concern"],
        "additionalProperties": False
    }
}

record_regulatory_question_json = {
    "name": "record_regulatory_question",
    "description": "Use this tool when you cannot answer a regulatory or compliance question",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The regulatory question that couldn't be answered"
            }
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

analyze_drug_profile_json = {
    "name": "analyze_drug_profile",
    "description": "Analyze a drug profile PDF and generate development strategies. Use when user mentions they have a drug profile document or asks to analyze an uploaded file.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to the uploaded PDF file"
            }
        },
        "required": ["file_path"],
        "additionalProperties": False
    }
}

# Combine all tools
tools = [
    {"type": "function", "function": record_strategy_decision_json},
    {"type": "function", "function": record_safety_concern_json},
    {"type": "function", "function": record_regulatory_question_json},
    {"type": "function", "function": analyze_drug_profile_json}
]

def handle_tool_calls(tool_calls):
    """Handle tool calls from the LLM - Ed's Lab 4 pattern"""
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        print(f"🔧 Tool called: {tool_name}", flush=True)
        
        # Get the function from globals and call it
        tool_function = globals().get(tool_name)
        result = tool_function(**arguments) if tool_function else {"error": "tool not found"}
        
        results.append({
            "role": "tool",
            "content": json.dumps(result),
            "tool_call_id": tool_call.id
        })
    return results

def create_system_prompt():
    """Create system prompt for conversational drug development assistant"""
    return """You are a pharmaceutical development strategy advisor AI assistant.

Your role is to help users think through drug development strategies through conversation.

CAPABILITIES:
- Discuss drug development strategies, clinical trials, regulatory pathways
- Analyze drug profiles when users provide information
- Generate and compare multiple development strategies
- Answer questions about pharma regulations, trial design, market access

TOOLS YOU MUST USE:
- Use record_strategy_decision when a user decides on a specific development strategy
- Use record_safety_concern when safety issues are discussed
- Use record_regulatory_question when you cannot answer a regulatory question

CONVERSATION STYLE:
- Be professional but conversational
- Ask clarifying questions about the drug, indication, stage of development
- Offer to analyze documents if users mention they have drug profiles or clinical data
- Guide users through strategic thinking rather than just giving answers
- If you don't know something regulatory-specific, acknowledge it and use your tool

Start by asking the user what drug or therapeutic area they're working on."""

def chat_with_tools(message, history):
    """Conversational chat with tool calling support - Lab 4 pattern"""
    
    # Build messages with system prompt
    messages = [{"role": "system", "content": create_system_prompt()}]
    
    # Add conversation history
    messages.extend(history)
    
    # Add current user message
    messages.append({"role": "user", "content": message})
    
    # Loop until LLM stops calling tools
    done = False
    while not done:
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=messages,
            tools=tools  # This enables tool calling!
        )
        
        finish_reason = response.choices[0].finish_reason
        
        if finish_reason == "tool_calls":
            # LLM wants to call tools - handle them
            message_with_tools = response.choices[0].message
            tool_calls = message_with_tools.tool_calls
            
            # Execute the tools
            tool_results = handle_tool_calls(tool_calls)
            
            # Add tool call and results to messages
            messages.append(message_with_tools)
            messages.extend(tool_results)
        else:
            # LLM is done, return the response
            done = True
    
    return response.choices[0].message.content


def render_tab():
    """Render conversational drug development assistant with PDF upload - Lab 4 style"""
    
    with gr.Column():
        gr.Markdown("""
        # 💊 Drug Development Strategy Assistant
        
        **Conversational AI for pharmaceutical development planning**
        
        I can help you:
        - Discuss drug development strategies
        - Analyze drug profiles and clinical data (upload PDF below)
        - Compare regulatory pathways
        - Think through trial design options
        
        *Upload a drug profile PDF or just start chatting!*
        """)
        
        # Add file upload
        file_upload = gr.File(label="📄 Upload Drug Profile PDF (optional)", file_types=[".pdf"])
        uploaded_file_state = gr.State()
        
        # Store file path when uploaded
        def handle_upload(file):
            if file:
                print(f"✅ File uploaded: {file.name}")
                return file.name
            return None
        
        file_upload.upload(handle_upload, inputs=file_upload, outputs=uploaded_file_state)
        
        # Create chatbot interface
        chatbot = gr.Chatbot(type="messages", height=500)
        
        msg = gr.Textbox(
            placeholder="Tell me about your drug, or ask me to analyze the uploaded PDF...",
            label="Your Message",
            lines=2
        )
        
        # Buttons
        with gr.Row():
            submit = gr.Button("Send", variant="primary")
            clear = gr.Button("Clear Conversation")
        
        def respond(message, history, file_path):
            """Handle user message and get response"""
            if history is None:
                history = []
            
            # If file was uploaded and user asks to analyze, include file path in message
            if file_path and any(keyword in message.lower() for keyword in ["analyze", "pdf", "profile", "document", "file"]):
                message += f"\n[System: User uploaded file at path: {file_path}]"
            
            try:
                # Get response using tool-enabled chat
                response = chat_with_tools(message, history)
                
                # Update history
                history.append({"role": "user", "content": message})
                history.append({"role": "assistant", "content": response})
                
                return history, ""
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                print(f"Error: {e}")
                history.append({"role": "user", "content": message})
                history.append({"role": "assistant", "content": error_msg})
                return history, ""
        
        # Wire up the interface
        msg.submit(respond, [msg, chatbot, uploaded_file_state], [chatbot, msg])
        submit.click(respond, [msg, chatbot, uploaded_file_state], [chatbot, msg])
        clear.click(lambda: ([], "", None), outputs=[chatbot, msg, uploaded_file_state])