from fastapi import FastAPI
from typing import Optional
from .database import get_simulated_ads, get_prompts
from agents.supervisor import SupervisorAgent

app = FastAPI(title="Lead Generator Ads API")

@app.get("/campaigns")
def campaigns(category: Optional[str] = None):
    df = get_simulated_ads()
    if df.empty:
        return []
    if category:
        df = df[df["category"].str.lower() == category.lower()]
    agg = (df.groupby(["campaign_id", "campaign_name", "category", "platform"], as_index=False)
             .agg({"spend":"sum", "clicks":"sum", "leads":"sum"}))
    return agg.to_dict(orient="records")

@app.get("/metrics/monthly")
def monthly_metrics():
    df = get_simulated_ads()
    if df.empty:
        return []
    keep = ["month", "category", "campaign_id", "campaign_name", "platform", "spend", "cpc", "clicks", "leads", "cpl"]
    return df[keep].to_dict(orient="records")

@app.post("/prompts")
def submit_prompt(prompt: str, platform: str = "Google Ads"):
    sup = SupervisorAgent()
    result = sup.submit_prompt(prompt, platform=platform)
    return result

@app.get("/prompts")
def list_prompts():
    df = get_prompts()
    if df.empty:
        return []
    return df.to_dict(orient="records")
