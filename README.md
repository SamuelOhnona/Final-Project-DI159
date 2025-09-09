
# Lead Generator Ads — Multi‑Agent System (Google/Meta)

Author: Samuel Ohnona  
Pitch: An AI-powered, multi-agent system that simulates and orchestrates lead generation campaigns across Google Ads and Meta Ads.  
Scope: Data Engineering project with end-to-end pipeline: prompt → plan → keywords → creatives → bidding → data storage → visualization.

---

## What this project includes
- Agents
  - SupervisorAgent: Orchestrates campaigns from a natural-language prompt (e.g., "Create a lead-gen campaign in Rhône-Alpes for TNS insurance").
  - KeywordAgent: Proposes relevant keywords, estimates intent and quality.
  - CreativeAgent: Generates ad copy (and image prompts) using OpenAI if available, or a mock fallback.
  - BidManagerAgent: Recommends bid adjustments/budget split based on performance.
- Simulation
  - simulate_data.py: Generates a full year of realistic multi-campaign performance with a $240k annual budget.
  - Creates: campaigns/simulated_ads.csv, campaigns/prompts_log.csv, and per-category splits in campaigns/categories/.
- Visualization
  - notebooks/viz_performance.ipynb: Monthly KPIs (Leads, CPC, CPL).
  - notebooks/viz_campaigns.ipynb: Category/Campaign comparisons.
  - app/streamlit_dashboard.py: Client-friendly dashboard.
- API
  - app/api.py (FastAPI): simple JSON endpoints for campaigns and metrics.

---

## Tech stack
- Python: pandas, numpy, matplotlib
- UX: Streamlit
- API: FastAPI + uvicorn
- AI: openai (optional; mocked if no key)
- Config: python-dotenv
- Data: CSV-based storage (SQLite/SQLAlchemy optional)

---

## Setup

```bash
# 1) Create a virtual env (recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Copy .env example and put your OpenAI key (optional)
cp .env.example .env
# then edit .env and set OPENAI_API_KEY=...

# 4) (Re)generate sample data for the last 12 full months
python simulate_data.py
```
The simulator will create:
- campaigns/prompts_log.csv
- campaigns/simulated_ads.csv
- campaigns/categories/banque.csv, assurance.csv, travaux.csv, immobilier.csv

---

## Run the dashboard (Streamlit)

```bash
streamlit run app/streamlit_dashboard.py
```

---

## Run the API (FastAPI)

```bash
uvicorn app.api:app --reload --port 8000
```

---

## Project structure
```
lead-generator-ads/
├── agents/
│   ├── bid_manager.py
│   ├── creative_agent.py
│   ├── keyword_agent.py
│   ├── supervisor.py
│   └── __init__.py
├── app/
│   ├── api.py
│   ├── database.py
│   └── streamlit_dashboard.py
├── campaigns/
│   ├── categories/
│   ├── prompts_log.csv         # (auto-generated)
│   └── simulated_ads.csv       # (auto-generated)
├── data/
│   └── keywords_seed.csv
├── notebooks/
│   ├── viz_campaigns.ipynb
│   └── viz_performance.ipynb
├── tests/
│   ├── test_agents.py
│   └── test_data.py
├── scripts/
│   └── reset_data.py
├── config.py
├── simulate_data.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Resetting the model for production
To ship a clean commercial baseline without historical data:
```bash
python scripts/reset_data.py
```
This will empty CSVs and keep the structure.

---

## Notes for your presentation (7–10 min)
- Frame the business problem: too much manual work to launch/optimize ads at scale.
- Show your agent architecture and how a prompt flows through the system.
- Highlight the year-long simulation: multi-campaign, budget usage, realistic CTR/CPC/CVR.
- Demo Streamlit dashboard and mention the API.
- Close with next steps: real Google/Meta APIs, persistence (PostgreSQL), alerting, governance (prompt logs).
