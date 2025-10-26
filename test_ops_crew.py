#!/usr/bin/env python
"""Quick test of Ops Team Crew with real data"""

import json
import pandas as pd
from pathlib import Path

# Load our enhanced data
data_dir = Path("data")

print("📊 TESTING OPS TEAM CREW WITH REAL DATA\n")
print("=" * 60)

# Test 1: Load trials data
print("\n✅ TEST 1: Clinical Data")
trials_df = pd.read_csv(data_dir / "trials.csv")
print(f"  - Loaded {len(trials_df)} trial sites")
print(f"  - Total enrolled: {trials_df['enrolled'].sum()}/788")
print(f"  - RED FLAG: {trials_df[trials_df['dropout_rate'] > 10]['site_name'].values}")

# Test 2: Load drug profile
print("\n✅ TEST 2: Drug Profile Data")
with open(data_dir / "drug_profile.json") as f:
    drug = json.load(f)
print(f"  - Drug: {drug['name']}")
print(f"  - Stage: {drug['stage']}")
print(f"  - Manufacturing capacity: {drug['manufacturing_operations']['current_capacity']['phase_iib_production']}")
print(f"  - Expansion needed: ${drug['manufacturing_operations']['phase_iii_requirements']['expansion_investment_usd']:,}")

# Test 3: Load KOL data
print("\n✅ TEST 3: KOL Data")
kols_df = pd.read_csv(data_dir / "doctors.csv")
print(f"  - Loaded {len(kols_df)} KOLs")
print(f"  - Avg influence score: {kols_df['influence_score'].mean():.1f}")
print(f"  - Phase IIb investigators: {kols_df['phase_iib_investigator'].sum()}")

print("\n" + "=" * 60)
print("\n✅ ALL DATA LOADED SUCCESSFULLY!")
print("\nCrew is ready to analyze:")
print("  1️⃣  Clinical Ops → Trial site analysis")
print("  2️⃣  Regulatory Ops → CMC + compliance assessment")
print("  3️⃣  Manufacturing Ops → Capacity planning")
print("  4️⃣  Commercial Ops → KOL strategy")
print("  5️⃣  Ops Manager → Go/No-Go decision")