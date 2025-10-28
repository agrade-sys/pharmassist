import os
import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

def respond(message, history):
    """Simple chat with OpenAI"""
    try:
        # Build messages from history
        messages = [
            {"role": "system", "content": "You are a pharmaceutical development strategy advisor. Help users think through drug development strategies, clinical trials, and regulatory pathways."}
        ]
        
        # Add conversation history
        for user_msg, assistant_msg in history:
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": assistant_msg})
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
        # Get response
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=500
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error: {str(e)}"

def render_tab():
    gr.Markdown("""
    # 💊 Drug Development Strategy Assistant
    
    **Conversational AI for pharmaceutical development planning**
    
    Ask me about:
    - Drug development strategies
    - Clinical trial design
    - Regulatory pathways
    - Market access strategies
    """)
    
    gr.ChatInterface(
        respond,
        chatbot=gr.Chatbot(height=500),
        textbox=gr.Textbox(placeholder="Ask about drug development strategies..."),
    )