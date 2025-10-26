import gradio as gr
import json
import pandas as pd
from pathlib import Path
from typing import Annotated, Any, Dict, List, Literal
from typing_extensions import TypedDict
from dotenv import load_dotenv

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel, Field

load_dotenv()

# ============================================================================
# STEP 1: Define State Object (Ed's Pattern)
# ============================================================================

class RiskAssessment(BaseModel):
    """Risk assessment output"""
    risk_level: str = Field(description="HIGH, MEDIUM, or LOW")
    risk_factors: List[str] = Field(description="Key risk factors identified")
    mitigation_strategy: str = Field(description="How to mitigate risks")

class SafetyReview(BaseModel):
    """Safety review output"""
    safety_status: str = Field(description="ACCEPTABLE, REQUIRES_MONITORING, or CONCERNING")
    adverse_events_summary: str = Field(description="Summary of AEs and SAEs")
    monitoring_recommendations: List[str] = Field(description="Specific monitoring needs")

class FinalRecommendation(BaseModel):
    """Final Phase III readiness recommendation"""
    go_no_go: str = Field(description="GO, CONDITIONAL_GO, or NO_GO")
    confidence_level: str = Field(description="HIGH, MEDIUM, or LOW")
    critical_actions: List[str] = Field(description="Must-do items before Phase III")
    executive_summary: str = Field(description="1-2 sentence summary for leadership")

class State(TypedDict):
    """LangGraph State for Trial Analysis"""
    messages: Annotated[List[Any], add_messages]
    trial_data: Dict[str, Any]
    drug_profile: Dict[str, Any]
    
    # Analysis outputs
    initial_analysis: str
    risk_assessment: RiskAssessment | None
    safety_review: SafetyReview | None
    final_recommendation: FinalRecommendation | None
    
    # Routing flags
    has_high_risk: bool
    has_safety_concerns: bool
    analysis_complete: bool


# ============================================================================
# STEP 2: Load Data Tools
# ============================================================================

data_dir = Path("data")

def load_trial_data() -> Dict[str, Any]:
    """Load trial CSV data"""
    df = pd.read_csv(data_dir / "trials.csv")
    return {
        "total_sites": len(df),
        "total_enrolled": df['enrolled'].sum(),
        "enrollment_target": df['enrollment_target'].sum(),
        "enrollment_pct": round(df['enrolled'].sum() / df['enrollment_target'].sum() * 100, 1),
        "sites": df.to_dict('records'),
        "high_dropout_sites": df[df['dropout_rate'] > 10]['site_name'].tolist(),
        "sites_with_violations": df[df['protocol_violations'] > 2]['site_name'].tolist(),
        "total_saes": df['serious_adverse_events'].sum(),
        "average_dropout_rate": round(df['dropout_rate'].mean(), 1),
        "efficacy_range": f"8.9-12.1%"
    }

def load_drug_profile() -> Dict[str, Any]:
    """Load drug profile JSON"""
    with open(data_dir / "drug_profile.json") as f:
        return json.load(f)

# ============================================================================
# STEP 3: Create Nodes (Ed's Pattern - Multiple Specialized Nodes)
# ============================================================================

llm = ChatOpenAI(model="gpt-4o-mini")

def trial_analyzer_node(state: State) -> State:
    """
    Node 1: Initial trial data analysis.
    Determines if there are high-risk factors or safety concerns.
    """
    trial_data = state["trial_data"]
    
    analysis = f"""
📊 TRIAL DATA SNAPSHOT:
- Enrollment: {trial_data['total_enrolled']}/{trial_data['enrollment_target']} ({trial_data['enrollment_pct']}%)
- Sites: {trial_data['total_sites']}
- High-Dropout Sites (>10%): {len(trial_data['high_dropout_sites'])} - {', '.join(trial_data['high_dropout_sites']) if trial_data['high_dropout_sites'] else 'None'}
- Protocol Violations: {len(trial_data['sites_with_violations'])} sites
- Total SAEs: {trial_data['total_saes']}
- Efficacy: {trial_data['efficacy_range']} LVEF improvement
"""
    
    # Determine routing flags
    has_high_risk = len(trial_data['high_dropout_sites']) > 0 or len(trial_data['sites_with_violations']) > 0
    has_safety_concerns = trial_data['total_saes'] > 2
    
    return {
        "messages": [{"role": "assistant", "content": analysis}],
        "initial_analysis": analysis,
        "has_high_risk": has_high_risk,
        "has_safety_concerns": has_safety_concerns
    }

def risk_assessment_node(state: State) -> State:
    """
    Node 2: Deep risk assessment for sites with issues.
    Triggered by has_high_risk flag.
    """
    llm_with_output = llm.with_structured_output(RiskAssessment)
    
    trial_data = state["trial_data"]
    prompt = f"""As a clinical trial risk assessor, evaluate these trial site issues:

High-Dropout Sites: {trial_data['high_dropout_sites']}
Sites with Protocol Violations: {trial_data['sites_with_violations']}
Average Dropout Rate: {trial_data['average_dropout_rate']}%

Provide a risk assessment and mitigation strategy."""
    
    risk_assessment = llm_with_output.invoke(prompt)
    
    return {
        "messages": [{"role": "assistant", "content": f"Risk Level: {risk_assessment.risk_level}"}],
        "risk_assessment": risk_assessment
    }

def safety_review_node(state: State) -> State:
    """
    Node 3: Safety review for trials with adverse events.
    Triggered by has_safety_concerns flag.
    """
    llm_with_output = llm.with_structured_output(SafetyReview)
    
    trial_data = state["trial_data"]
    drug_profile = state["drug_profile"]
    
    prompt = f"""As a clinical safety officer, review this trial safety profile:

Total SAEs: {trial_data['total_saes']}
SAE Rate: {round(trial_data['total_saes'] / max(trial_data['total_enrolled'], 1) * 100, 2)}%
Known Safety Issues: {drug_profile.get('safety_profile', {}).get('serious_adverse_events', [])}

Provide a safety assessment and monitoring recommendations."""
    
    safety_review = llm_with_output.invoke(prompt)
    
    return {
        "messages": [{"role": "assistant", "content": f"Safety Status: {safety_review.safety_status}"}],
        "safety_review": safety_review
    }

def final_recommendation_node(state: State) -> State:
    """
    Node 4: Synthesize all assessments into final Phase III readiness decision.
    Integrates outputs from risk and safety nodes.
    """
    llm_with_output = llm.with_structured_output(FinalRecommendation)
    
    trial_data = state["trial_data"]
    drug_profile = state["drug_profile"]
    
    # Build context
    context = f"""
PHASE III READINESS ASSESSMENT

Enrollment: {trial_data['enrollment_pct']}% complete
Risk Level: {state['risk_assessment'].risk_level if state['risk_assessment'] else 'N/A'}
Safety Status: {state['safety_review'].safety_status if state['safety_review'] else 'ACCEPTABLE'}
Efficacy Signal: {trial_data['efficacy_range']} LVEF improvement

Manufacturing Readiness: {drug_profile.get('manufacturing_operations', {}).get('manufacturing_readiness', 'UNKNOWN')}
Regulatory Status: {drug_profile.get('regulatory_operations', {}).get('submission_readiness', 'UNKNOWN')}
Commercial Readiness: {drug_profile.get('commercial_operations', {}).get('commercial_readiness', 'UNKNOWN')}

Make a GO/CONDITIONAL_GO/NO_GO recommendation for Phase III with confidence level."""
    
    prompt = f"""You are the Chief Clinical Officer evaluating Phase III initiation:

{context}

Provide your final recommendation considering all factors above."""
    
    recommendation = llm_with_output.invoke(prompt)
    
    return {
        "messages": [{"role": "assistant", "content": f"DECISION: {recommendation.go_no_go}"}],
        "final_recommendation": recommendation,
        "analysis_complete": True
    }

# ============================================================================
# STEP 4: Create Conditional Edge Routers
# ============================================================================

def route_after_initial_analysis(state: State) -> List[str]:
    """
    Router 1: After initial analysis, route to risk and/or safety nodes.
    Can send to multiple nodes in parallel (returns list).
    """
    next_nodes = []
    if state["has_high_risk"]:
        next_nodes.append("risk_assessment")
    if state["has_safety_concerns"]:
        next_nodes.append("safety_review")
    
    # If no issues, go straight to recommendation
    if not next_nodes:
        next_nodes.append("final_recommendation")
    
    return next_nodes

def route_to_final_recommendation(state: State) -> str:
    """
    Router 2: After risk/safety assessments, always go to final recommendation.
    """
    return "final_recommendation"

# ============================================================================
# STEP 5: Build Graph (Ed's 5-Step Pattern)
# ============================================================================

def create_trial_graph():
    """
    Creates the LangGraph workflow with branching logic.
    
    Step 1: Define State ✓
    Step 2: Start Graph Builder ✓
    Step 3: Create Nodes ✓
    Step 4: Create Edges with Conditional Routing ✓
    Step 5: Compile ✓
    """
    # Step 2: Initialize Graph Builder with State
    graph_builder = StateGraph(State)
    
    # Step 3: Add Nodes
    graph_builder.add_node("trial_analyzer", trial_analyzer_node)
    graph_builder.add_node("risk_assessment", risk_assessment_node)
    graph_builder.add_node("safety_review", safety_review_node)
    graph_builder.add_node("final_recommendation", final_recommendation_node)
    
    # Step 4: Create Edges with Conditional Routing
    graph_builder.add_edge(START, "trial_analyzer")
    
    # Conditional edges: analyzer can route to multiple nodes
    graph_builder.add_conditional_edges(
        "trial_analyzer",
        route_after_initial_analysis,
        {
            "risk_assessment": "risk_assessment",
            "safety_review": "safety_review",
            "final_recommendation": "final_recommendation"
        }
    )
    
    # Risk and Safety nodes route to final recommendation
    graph_builder.add_edge("risk_assessment", "final_recommendation")
    graph_builder.add_edge("safety_review", "final_recommendation")
    
    # Final node goes to END
    graph_builder.add_edge("final_recommendation", END)
    
    # Step 5: Compile the Graph
    graph = graph_builder.compile()
    
    return graph

# ============================================================================
# STEP 6: Gradio Interface
# ============================================================================

def render_tab():
    """Render the Trial Agent tab in Gradio"""
    
    with gr.Group():
        gr.Markdown("""
        ## 🔬 Clinical Trials Agent - Phase IIb Analysis
        
        **LangGraph Pattern (Week 4)**: Graph-based workflow with conditional branching
        
        Demonstrates:
        - ✅ State management with TypedDict
        - ✅ Multiple specialized nodes
        - ✅ Conditional edge routing (branching logic)
        - ✅ Structured Pydantic outputs
        - ✅ Graph visualization support
        """)
        
        with gr.Row():
            analyze_button = gr.Button("📊 Analyze Trial Data", size="lg")
        
        output = gr.Textbox(
            label="Phase III Readiness Assessment",
            lines=25,
            interactive=False,
            placeholder="Click 'Analyze Trial Data' to generate comprehensive assessment..."
        )
        
        def run_trial_analysis():
            """Execute the LangGraph workflow with branching"""
            try:
                # Load data
                trial_data = load_trial_data()
                drug_profile = load_drug_profile()
                
                # Create and run graph
                graph = create_trial_graph()
                initial_state = State(
                    messages=[],
                    trial_data=trial_data,
                    drug_profile=drug_profile,
                    initial_analysis="",
                    risk_assessment=None,
                    safety_review=None,
                    final_recommendation=None,
                    has_high_risk=False,
                    has_safety_concerns=False,
                    analysis_complete=False
                )
                
                result = graph.invoke(initial_state)
                
                # Format comprehensive output
                output_text = f"""
{'='*70}
🏥 PHASE III READINESS ASSESSMENT REPORT
{'='*70}

📋 INITIAL ANALYSIS:
{result['initial_analysis']}

{'='*70}
⚠️  RISK ASSESSMENT:
Risk Level: {result['risk_assessment'].risk_level if result['risk_assessment'] else 'N/A'}
Issues: {', '.join(result['risk_assessment'].risk_factors) if result['risk_assessment'] else 'None identified'}
Mitigation: {result['risk_assessment'].mitigation_strategy if result['risk_assessment'] else 'N/A'}

{'='*70}
🔬 SAFETY REVIEW:
Status: {result['safety_review'].safety_status if result['safety_review'] else 'ACCEPTABLE'}
Summary: {result['safety_review'].adverse_events_summary if result['safety_review'] else 'No concerns'}
Recommendations:
{chr(10).join(f'  • {rec}' for rec in (result['safety_review'].monitoring_recommendations or [])) if result['safety_review'] else '  • Continue standard monitoring'}

{'='*70}
🚀 FINAL RECOMMENDATION:
Decision: {result['final_recommendation'].go_no_go}
Confidence: {result['final_recommendation'].confidence_level}
Executive Summary: {result['final_recommendation'].executive_summary}

Critical Actions:
{chr(10).join(f'{i+1}. {action}' for i, action in enumerate(result['final_recommendation'].critical_actions))}

{'='*70}
"""
                return output_text
                
            except Exception as e:
                import traceback
                return f"❌ Error: {str(e)}\n\n{traceback.format_exc()}"
        
        analyze_button.click(
            fn=run_trial_analysis,
            outputs=output
        )