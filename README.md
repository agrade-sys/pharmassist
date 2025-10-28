---
title: Pharmassist
emoji: 🏥
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.44.1
app_file: app.py
pinned: false
---

# Pharmassist — Agentic Drug Launch Assistant

A pharmaceutical AI application demonstrating agentic AI patterns learned from [The Complete Agentic AI Engineering Course (2025)] by Ed Donner. This project applies course concepts to real-world drug development workflows.

🔗 **Live Demo**: https://huggingface.co/spaces/saimon-agrade/pharmassist

## 🎯 Project Overview

Pharmassist is a multi-agent system that assists pharmaceutical teams through the drug launch lifecycle, from initial strategy development through regulatory approval and market launch. Each agent demonstrates specific agentic AI patterns and techniques from the course.

## 📚 Implemented Agents

### Week 1: Drug Profile Agent ✅
**Conversational AI Drug Development Advisor**

**Demonstrates:** OpenAI API integration, ChatInterface pattern, conversation management

**Key Features:**
- Interactive AI advisor for drug development strategies
- Discusses clinical trials, regulatory pathways, and market strategies
- Natural conversation flow with context retention
- Real-time responses using GPT-4o-mini

**How to Test:**
Start a conversation about drug development! Try these scenarios:

**Scenario 1: New Drug Development**
```
User: "I'm developing a novel drug for chronic heart failure. 
It's a selective Beta-3 adrenergic receptor agonist. 
We've completed Phase IIa with promising LVEF improvements. 
What should be my next steps?"
```

**Scenario 2: Regulatory Strategy**
```
User: "We have strong efficacy data in European trials. 
Should we pursue EMA approval first or go straight for FDA? 
Our drug targets NYHA Class II-III heart failure patients."
```

**Scenario 3: Safety Concerns**
```
User: "We observed mild arrhythmia in 2% of elderly patients 
during Phase II trials. How should this impact our Phase III design? 
Should we exclude patients over 75?"
```

**Scenario 4: Market Strategy**
```
User: "Our main competitors are Entresto and Verquvo. 
How can we differentiate? Our drug shows better tolerability 
but similar efficacy. What's our value proposition?"
```

**Technologies:** OpenAI API, Gradio ChatInterface, Python

**Status:** ✅ Deployed

---

### Week 2: Doctor Outreach Agent ✅
**Multi-Agent Email Generation System**

**Demonstrates:** OpenAI Agents SDK, multi-agent collaboration, structured outputs, Pydantic models

**Key Features:**
- Three specialized agents with different communication styles:
  - 🎩 **Formal Agent**: Professional, clinical communication
  - 🔬 **Scientific Agent**: Research-focused, data-driven
  - 🤝 **Engaging Agent**: Warm, relationship-building
- **Outreach Manager**: Evaluates all approaches and selects optimal email
- **Structured Output**: Consistent email format with Pydantic validation

**How to Test:**

**Test Case 1: Cardiologist Outreach**
```
Doctor Name: Dr. Sarah Chen
Specialty: Cardiology
```
Expected: Scientific or formal tone emphasizing LVEF data and cardiovascular outcomes

**Test Case 2: General Practitioner**
```
Doctor Name: Dr. Michael Rodriguez  
Specialty: General Practice
```
Expected: Engaging tone focusing on patient quality of life and practical benefits

**Test Case 3: Clinical Researcher**
```
Doctor Name: Dr. Aisha Patel
Specialty: Clinical Research
```
Expected: Scientific tone with trial methodology and statistical significance

**Technologies:** OpenAI Agents SDK, Pydantic, async/await

**Status:** ✅ Deployed

---

### Week 3-4: Clinical Trials Agent ✅
**Trial Design and Data Analysis**

**Demonstrates:** Data visualization, trial protocol analysis, statistical insights

**Key Features:**
- Clinical trial data visualization
- Patient enrollment tracking
- Adverse event monitoring
- Trial site performance analysis

**How to Test:**
Upload the sample `data/trials.csv` or explore the pre-loaded trial data visualizations.

**Technologies:** Gradio, Pandas, data visualization libraries

**Status:** ✅ Deployed

---

### Week 3-4: Ops Team Agent ✅
**Multi-Agent Team Coordination**

**Demonstrates:** Team coordination patterns, workflow management, multi-agent orchestration

**Key Features:**
- Coordinate multiple operational workflows
- Task assignment and tracking
- Cross-functional team collaboration
- Workflow automation

**Technologies:** Multi-agent coordination patterns

**Status:** ✅ Deployed

---

### Planned Agents (In Development)
- **Regulatory Brief** (Week 3-4): Regulatory strategy advisor
- **Flow Creator** (Week 6+): Dynamic workflow creation

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- OpenAI API key

### Installation
```bash
# Clone the repository
git clone https://github.com/agrade-sys/pharmassist.git
cd pharmassist

# Install dependencies with uv
uv sync

# Or with pip
pip install -r requirements.txt

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

## 💡 Sample Test Data

### For Drug Profile Agent

Use these realistic scenarios to test the conversational AI:

**CardioRelief Case Study**
```
Drug: CardioRelief
Indication: Chronic Heart Failure (NYHA Class II-III)
Stage: Phase IIb completed
Mechanism: Selective Beta-3 Adrenergic Receptor Agonist
Efficacy: 10% relative improvement in LVEF after 12 weeks
Safety: Mild dizziness (15%), headache (12%), rare arrhythmia (2%)
Target Markets: EU, Malaysia, Singapore
Competitors: Entresto, Verquvo
```

Ask the agent about:
- Optimal Phase III design
- Regulatory approval strategy (EMA vs FDA first)
- How to address safety signals
- Market differentiation strategies
- Patient recruitment strategies

---

### For Doctor Outreach Agent

**Test Physician Profiles:**

**Profile 1: Academic Cardiologist**
```
Name: Dr. Yuki Tanaka
Specialty: Interventional Cardiology
Institution: University Hospital Tokyo
Focus: Heart failure research, clinical trials
```

**Profile 2: Community Cardiologist**
```
Name: Dr. James O'Connor
Specialty: General Cardiology  
Institution: Community Heart Center
Focus: Patient care, treatment optimization
```

**Profile 3: GP with HF Focus**
```
Name: Dr. Maria Santos
Specialty: Family Medicine
Institution: Primary Care Clinic
Focus: Chronic disease management
```

---

## 🛠️ Technical Architecture

### Core Technologies
- **Gradio 4.44.1**: UI framework
- **OpenAI GPT-4o-mini**: Primary LLM
- **OpenAI Agents SDK**: Multi-agent framework
- **Pydantic**: Structured outputs
- **Python-dotenv**: Environment management

### Agentic Patterns Implemented

**Week 1:**
- ChatInterface for conversation management
- Stateful dialogue with context
- Real-time LLM integration

**Week 2:**
- Multi-agent collaboration
- Agent orchestration
- Structured outputs with Pydantic
- Async/await execution
- @function_tool decorator

**Week 3-4:**
- Data visualization and analysis
- Multi-agent team coordination
- Workflow automation

---

## 📊 Project Structure
```
pharmassist/
├── pharmassist_agents/
│   ├── drug_profile_agent.py    # Week 1 ✅
│   ├── outreach_agent.py        # Week 2 ✅
│   ├── trial_agent.py           # Week 3-4 ✅
│   ├── ops_team_agent.py        # Week 3-4 ✅
│   ├── regulatory_agent.py      # In development
│   └── creator_agent.py         # Planned
├── data/
│   ├── drug_profile.json
│   ├── doctors.csv
│   └── trials.csv
├── app.py
├── requirements.txt
└── README.md
```

---

## 🎓 Learning Objectives Demonstrated

### Week 1: Foundations ✅
- ✅ OpenAI API integration
- ✅ Gradio ChatInterface
- ✅ Conversation management
- ✅ Production deployment

### Week 2: OpenAI Agents SDK ✅
- ✅ Multi-agent collaboration
- ✅ Agent orchestration
- ✅ Structured outputs (Pydantic)
- ✅ Async/await patterns

### Week 3-4: Advanced Patterns ✅
- ✅ Data visualization
- ✅ Multi-agent coordination
- ✅ Workflow automation

---

## 🔍 Course Adaptations

**Drug Profile Agent** adapts Ed's career advisor pattern to pharmaceutical strategy consulting.

**Doctor Outreach Agent** adapts Ed's cold email SDR pattern to physician outreach with medical domain expertise.

**Clinical Trials & Ops Agents** demonstrate practical applications of multi-agent coordination in healthcare operations.

All patterns maintain Ed's core architectural principles while applying them to pharma-specific workflows.

---

## 🚀 Deployment

**Platform:** HuggingFace Spaces  
**Live URL:** https://huggingface.co/spaces/saimon-agrade/pharmassist  
**Secrets:** OPENAI_API_KEY configured in Space settings

---

## 📝 License

Apache License 2.0

---

## 🙏 Acknowledgments

Built as a learning demonstration for [The Complete Agentic AI Engineering Course (2025)] by Ed Donner on Udemy.

This project showcases how course patterns transfer to domain-specific applications in pharmaceutical development.

---

## 🔗 Links

- **Live Demo**: https://huggingface.co/spaces/saimon-agrade/pharmassist
- **GitHub**: https://github.com/agrade-sys/pharmassist
- **Course**: Ed Donner's Agentic AI Engineering Course (Udemy)

---

**Note**: Educational project for demonstrating agentic AI patterns. Not for actual pharmaceutical decisions.