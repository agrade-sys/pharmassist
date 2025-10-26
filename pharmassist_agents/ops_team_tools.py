"""Tools for Ops Team Crew"""

import json
import pandas as pd
from pathlib import Path
from crewai.tools import tool

data_dir = Path("data")

@tool
def read_trials_data():
    """Read and return Phase IIb trial site data"""
    df = pd.read_csv(data_dir / "trials.csv")
    return df.to_json(orient="records")

@tool
def read_drug_profile():
    """Read and return CardioRelief drug profile"""
    with open(data_dir / "drug_profile.json") as f:
        return json.dumps(json.load(f), indent=2)

@tool
def read_kol_database():
    """Read and return Key Opinion Leader database"""
    df = pd.read_csv(data_dir / "doctors.csv")
    return df.to_json(orient="records")

# Test the tools
if __name__ == "__main__":
    print("Testing tools...\n")
    
    print("✅ read_trials_data tool created")
    trials_df = pd.read_csv(data_dir / "trials.csv")
    print(f"   Loaded {len(trials_df)} sites")
    
    print("\n✅ read_drug_profile tool created")
    with open(data_dir / "drug_profile.json") as f:
        profile = json.load(f)
    print(f"   Drug: {profile['name']}")
    
    print("\n✅ read_kol_database tool created")
    kols_df = pd.read_csv(data_dir / "doctors.csv")
    print(f"   Loaded {len(kols_df)} KOLs")
    
    print("\n✅ All tools are ready for Crew agents!")