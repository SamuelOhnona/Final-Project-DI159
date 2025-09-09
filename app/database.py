"""Thin CSV-based storage facade.
You can replace by SQLAlchemy/PostgreSQL later without changing the app.
"""
import pandas as pd
import os

BASE = os.path.join("campaigns")
SIM_FILE = os.path.join(BASE, "simulated_ads.csv")
PROMPTS_FILE = os.path.join(BASE, "prompts_log.csv")

def get_simulated_ads():
    if not os.path.exists(SIM_FILE):
        return pd.DataFrame()
    return pd.read_csv(SIM_FILE)

def get_prompts():
    if not os.path.exists(PROMPTS_FILE):
        return pd.DataFrame()
    return pd.read_csv(PROMPTS_FILE)
