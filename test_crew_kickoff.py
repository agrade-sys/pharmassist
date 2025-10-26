#!/usr/bin/env python
"""Test running the Ops Team Crew with crew.kickoff()"""

import os
from dotenv import load_dotenv
from pharmassist_agents.ops_team_agent import create_ops_crew

load_dotenv()

# Verify OpenAI API key
if not os.getenv("OPENAI_API_KEY"):
    print("❌ ERROR: OPENAI_API_KEY not set in .env")
    print("   Please add your OpenAI API key to .env file")
    exit(1)

print("🚀 STARTING OPS TEAM CREW EXECUTION\n")
print("=" * 70)
print("Workflow:")
print("  1️⃣  Clinical Ops Agent → Analyzes trial sites")
print("  2️⃣  Regulatory Ops Agent → Assesses compliance")
print("  3️⃣  Manufacturing Ops Agent → Evaluates capacity")
print("  4️⃣  Commercial Ops Agent → Develops KOL strategy")
print("  5️⃣  Ops Manager → Synthesizes decision")
print("=" * 70)
print()

try:
    # Create and run crew
    crew = create_ops_crew()
    print("✅ Crew created successfully")
    print("⏳ Running crew.kickoff()... (this may take 2-3 minutes)\n")
    
    result = crew.kickoff()
    
    print("\n" + "=" * 70)
    print("✅ CREW EXECUTION COMPLETE\n")
    print("PHASE III GO/NO-GO DECISION:\n")
    print(result)
    print("\n" + "=" * 70)
    
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()