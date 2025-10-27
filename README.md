---
title: Pharmassist
emoji: 🏥
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: "4.44.1"
app_file: app.py
pinned: false
---

# Pharmassist — Agentic Drug Launch Assistant

A pharmaceutical AI application demonstrating agentic AI patterns learned from [The Complete Agentic AI Engineering Course (2025)] by Ed Donner. This project applies course concepts to real-world drug development workflows.

## 🎯 Project Overview

Pharmassist is a multi-agent system that assists pharmaceutical teams through the drug launch lifecycle, from initial strategy development through regulatory approval and market launch. Each agent demonstrates specific agentic AI patterns and techniques from the course.

## 📚 Course Learning Demonstrations

### Week 1: Foundations - Drug Profile Agent ✅
**Conversational AI Drug Development Advisor**

Demonstrates Week 1 Labs 1-4:
- **Lab 1**: OpenAI API integration, basic LLM calls
- **Lab 2**: Multi-candidate generation (3 development strategies), judgment pattern
- **Lab 3**: PDF processing (drug profiles), Gradio UI, state management
- **Lab 4**: Tool use with function calling, conversational agent pattern

**Key Features:**
- Conversational interface for discussing drug development strategies
- PDF analysis tool that generates 3 alternative development strategies
- Function calling with 4 tools:
  - `record_strategy_decision` - Logs when users commit to a strategy
  - `record_safety_concern` - Records safety issues raised
  - `record_regulatory_question` - Tracks unanswered regulatory questions
  - `analyze_drug_profile` - Processes uploaded drug profile PDFs

**Pattern Used:** Ed's career agent pattern adapted for pharma - conversational AI with manual tool calling for real-world actions.

**Technologies:** OpenAI API, Gradio, PyPDF, manual function calling pattern

**Status:** ✅ Complete and functional

---

### Week 2: OpenAI Agents SDK - Doctor Outreach Agent ✅
**Multi-Agent Email Generation System**

Demonstrates Week 2 Labs 2-3:
- **Lab 2**: OpenAI Agents SDK (Agent, Runner, @function_tool), multi-agent collaboration, agent-as-tool pattern, orchestration
- **Lab 3**: Structured outputs using Pydantic models

**Key Features:**
- Three competing outreach agents with different communication styles:
  - 🎩 **Formal Agent**: Professional, clinical peer-to-peer communication
  - 🔬 **Scientific Agent**: Research-focused, data-driven with trial results
  - 🤝 **Engaging Agent**: Warm, relationship-building, patient-focused
- **Outreach Manager Agent**: Evaluates all three approaches and selects the optimal email
- **Structured Email Output**: Pydantic models ensure consistent format (subject, body, tone)
- **Tool Integration**: 
  - `record_doctor_outreach` - Logs outreach generation
  - `flag_for_followup` - Marks doctors for manual follow-up

**Pattern Used:** Ed's cold email SDR pattern adapted for physician outreach - multiple specialized agents coordinated by a manager agent using handoffs and tools.

**Technologies:** OpenAI Agents SDK, Pydantic, async/await, @function_tool decorator

**Status:** ✅ Complete and functional

---

### Planned Agents (Future Weeks)
Building systematically as I progress through the course:
- **Regulatory Brief** (Week 3-4): Multi-agent regulatory strategy advisor
- **Clinical Trials** (Week 3-4): Trial design and data analysis
- **Ops Team** (Week 5): Multi-agent coordination and workflow orchestration
- **Flow Creator** (Week 6+): Dynamic workflow creation and execution

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- OpenAI API key

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/pharmassist.git
cd pharmassist

# Install dependencies
uv sync

# Set up environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Running Locally
```bash
python app.py
```

Navigate to `http://127.0.0.1:7860` in your browser.

---

## 💡 Usage

### Drug Profile Agent (Week 1)
1. Click on the "Drug Profile" tab
2. (Optional) Upload a drug profile PDF
3. Chat with the AI about your drug development strategy
4. Ask it to analyze uploaded PDFs: "Please analyze the PDF I uploaded"
5. Discuss strategies, safety concerns, and regulatory pathways
6. Watch the terminal for tool call logs

**Example Prompts:**
- "I'm developing a drug for chronic heart failure in NYHA Class II-III patients"
- "Please analyze the drug profile PDF I just uploaded"
- "I'm worried about potential arrhythmia events in elderly patients"
- "I've decided to proceed with a Phase III trial"

### Doctor Outreach Agent (Week 2)
1. Click on the "Doctor Outreach" tab
2. Enter doctor name and specialty
3. Click "Generate Outreach Email"
4. The system generates 3 different email approaches in parallel
5. Manager agent evaluates and selects the best one
6. Watch terminal for multi-agent process logs

**Example:**
- Doctor: Sarah Johnson
- Specialty: Cardiology
- Output: Professional email introducing CardioRelief drug with trial data

**Terminal Output Shows:**
```
🔄 Generating outreach for Dr. Sarah Johnson (Cardiology)...
📧 Outreach Generated: formal
📧 Outreach Generated: scientific  
📧 Outreach Generated: engaging
✅ Outreach complete!
```

**Check OpenAI Traces:** https://platform.openai.com/traces

---

## 🛠️ Technical Architecture

### Core Technologies
- **Gradio**: UI framework for rapid prototyping
- **OpenAI GPT-4o-mini**: Primary LLM for generation and decision-making
- **OpenAI Agents SDK**: Week 2+ framework for multi-agent systems
- **PyPDF**: PDF text extraction
- **Pydantic**: Structured outputs and data validation
- **Python-dotenv**: Environment management

### Agentic Patterns Implemented

**Week 1 Patterns:**
1. **Manual Tool Calling**: Function definitions with JSON schemas and if/else handling
2. **Reflection Pattern**: Multi-candidate strategy generation with evaluation
3. **Conversational Agent**: Stateful dialogue with memory
4. **Document Processing**: PDF parsing and content extraction

**Week 2 Patterns:**
1. **Multi-Agent Collaboration**: Multiple specialized agents working in parallel
2. **Agent-as-Tool Pattern**: Converting agents into callable tools using `.as_tool()`
3. **Orchestration**: Manager agent coordinating subordinate agents
4. **@function_tool Decorator**: Simplified tool definition (replaces JSON boilerplate)
5. **Structured Outputs**: Pydantic models for reliable, typed responses
6. **Async/Await**: Non-blocking agent execution with `Runner.run()`
7. **Tracing**: OpenAI platform integration for debugging and monitoring

---

## 📊 Project Structure
```
pharmassist/
├── pharmassist_agents/              # Agent implementations
│   ├── __init__.py
│   ├── drug_profile_agent.py        # Week 1 - Conversational + Manual Tools
│   ├── outreach_agent.py            # Week 2 - Multi-Agent SDK
│   ├── regulatory_agent.py          # Placeholder
│   ├── trial_agent.py               # Placeholder
│   ├── ops_team_agent.py            # Placeholder
│   └── creator_agent.py             # Placeholder
├── data/
│   ├── drug_profile.json            # Sample drug data (CardioRelief)
│   ├── doctors.csv                  # Sample doctor list
│   └── trials.csv                   # Sample trial data
├── app.py                           # Main Gradio application
├── pyproject.toml                   # Dependencies
├── .env.example                     # Environment template
└── README.md                        # This file
```

---

## 🎓 Learning Objectives Demonstrated

### Week 1: Foundations ✅
- ✅ OpenAI API integration and prompt engineering
- ✅ Multiple LLM call patterns (generation, evaluation)
- ✅ Gradio UI development with tabs and state management
- ✅ Manual tool use via function calling with JSON schemas
- ✅ PDF document processing
- ✅ Conversational agent with context retention

### Week 2: OpenAI Agents SDK ✅
- ✅ Agent, Runner, trace patterns
- ✅ @function_tool decorator (replaces manual JSON)
- ✅ Multi-agent collaboration
- ✅ Agent-as-tool pattern
- ✅ Manager/orchestration pattern
- ✅ Structured outputs with Pydantic
- ✅ Async/await execution model

### Weeks 3-6: Advanced Topics (Planned)
- 🔄 CrewAI framework for role-based agents
- 🔄 LangGraph for workflow orchestration
- 🔄 AutoGen for conversational agents
- 🔄 MCP (Model Context Protocol)
- 🔄 RAG and knowledge bases
- 🔄 Production deployment

---

## 🔍 Key Adaptations from Course Examples

### Week 1: Career Agent → Drug Profile Agent

| Ed's Career Agent | Pharmassist Drug Profile |
|------------------|-------------------------|
| LinkedIn PDF processing | Drug profile PDF processing |
| Career Q&A chatbot | Drug strategy advisor |
| `record_user_details(email)` | `record_strategy_decision(strategy)` |
| `record_unknown_question()` | `record_regulatory_question()` |
| Manual pushover notifications | Console logging with tool calls |
| - | `record_safety_concern()` |
| - | `analyze_drug_profile()` |

### Week 2: Cold Email SDR → Doctor Outreach Agent

| Ed's Sales Agents | Pharmassist Doctor Outreach |
|------------------|---------------------------|
| Professional Sales Agent | Formal Outreach Agent |
| Engaging Sales Agent | Engaging Outreach Agent |
| Busy Sales Agent | Scientific Outreach Agent |
| Sales Manager picks best email | Outreach Manager picks best email |
| SendGrid email sending | Console logging (SendGrid optional) |
| Email formatter agent (handoff) | Structured Pydantic output |

**Core patterns are identical** - demonstrating understanding of foundational concepts while applying them to pharmaceutical domain-specific challenges.

---

## 🚧 Development Roadmap

**Completed:**
- [x] Week 1: Drug Profile Agent with conversational AI and manual tools
- [x] Week 2: Doctor Outreach Agent with multi-agent SDK and structured outputs

**Next Steps:**
- [ ] Week 3-4: Additional framework implementations (CrewAI, LangGraph)
- [ ] Regulatory Brief Agent for multi-step approval workflows
- [ ] Clinical Trials Agent for data analysis
- [ ] Ops Team multi-agent coordination

**Future Enhancements:**
- [ ] Add evaluation systems with retry logic
- [ ] Implement RAG for medical knowledge bases
- [ ] Add database persistence for agent actions
- [ ] Deploy to HuggingFace Spaces or similar
- [ ] Complete workflow orchestration system

---

## 📝 License

Apache License 2.0

---

## 🙏 Acknowledgments

This project is built as a learning demonstration for [The Complete Agentic AI Engineering Course (2025)] by Ed Donner on Udemy. All core patterns and techniques are adapted from the course materials and applied to pharmaceutical development workflows.

The project showcases how course concepts transfer to domain-specific applications, demonstrating both technical understanding and practical adaptation skills.

**Course Link:** [The Complete Agentic AI Engineering Course (2025)]

---

**Note**: This is an educational project demonstrating agentic AI patterns. It is not intended for actual pharmaceutical development decisions. Always consult qualified professionals for drug development strategies.

---

## 🔗 Connect

Building in public as I learn. Follow my progress!

- LinkedIn: [Your LinkedIn]
- GitHub: [Your GitHub]

**Tags:** #AgenticAI #OpenAI #Python #Gradio #LLM #MultiAgent #Pharmaceutical #MachineLearning