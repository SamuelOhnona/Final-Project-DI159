import os
import csv
import random
import pandas as pd

os.makedirs('campaigns/categories', exist_ok=True)

# Determine the last 12 full months relative to today
today = pd.Timestamp.today().normalize()
end_last_full_month = pd.Timestamp(today.year, today.month, 1) - pd.offsets.Day(1)
months = pd.date_range(end=end_last_full_month, periods=12, freq='M')

# Annual budget
ANNUAL_BUDGET = 240_000  # USD
MONTHLY_BUDGET = ANNUAL_BUDGET // 12

random.seed(int(os.getenv('SIMULATION_RANDOM_SEED', '42')))

CATEGORIES = ['Banque', 'Assurance', 'Travaux', 'Immobilier']
PLATFORMS = ['Google Ads', 'Meta Ads']

# Define 2 campaigns per category for realism
CAMPAIGNS = []
for cat in CATEGORIES:
    for i in range(1, 3):
        platform = random.choice(PLATFORMS)
        CAMPAIGNS.append({
            'campaign_id': f"{cat[:3].upper()}-{i:02d}",
            'campaign_name': f"{cat} {i} ({platform})",
            'category': cat,
            'platform': platform,
        })

# Category/base conversion priors (roughly realistic)
CATEGORY_CVR = {
    'Banque': (0.02, 0.05),
    'Assurance': (0.03, 0.07),
    'Travaux': (0.025, 0.06),
    'Immobilier': (0.02, 0.05),
}
# CPC priors by platform
CPC_RANGE = {
    'Google Ads': (1.5, 4.0),
    'Meta Ads': (0.7, 2.5),
}

rows = []
# Allocate monthly budget across campaigns using simple random weights
for m in months:
    weights = [random.uniform(0.8, 1.2) for _ in CAMPAIGNS]
    s = sum(weights)
    allocs = [MONTHLY_BUDGET * (w/s) for w in weights]
    for camp, spend in zip(CAMPAIGNS, allocs):
        platform = camp['platform']
        cpc_low, cpc_high = CPC_RANGE[platform]
        cpc = round(random.uniform(cpc_low, cpc_high), 2)
        clicks = int(spend / cpc) if cpc > 0 else 0

        # derive CTR by platform/cat (for info only)
        ctr = random.uniform(0.008, 0.04)  # 0.8%..4%
        impressions = int(clicks / ctr) if ctr > 0 else clicks * 100

        # conversions/leads
        cvr_low, cvr_high = CATEGORY_CVR[camp['category']]
        cvr = random.uniform(cvr_low, cvr_high)
        leads = int(clicks * cvr)
        cpl = round(spend / leads, 2) if leads > 0 else 0.0

        rows.append({
            'month': m.strftime('%Y-%m'),
            'category': camp['category'],
            'campaign_id': camp['campaign_id'],
            'campaign_name': camp['campaign_name'],
            'platform': platform,
            'spend': round(spend, 2),
            'cpc': cpc,
            'clicks': clicks,
            'ctr': round(ctr, 4),
            'impressions': impressions,
            'leads': leads,
            'cpl': cpl,
        })

df = pd.DataFrame(rows)
df = df.sort_values(['month','category','campaign_id']).reset_index(drop=True)
df.to_csv('campaigns/simulated_ads.csv', index=False)

# Create per-category splits
for cat in CATEGORIES:
    df[df['category'] == cat].to_csv(f'campaigns/categories/{cat.lower()}.csv', index=False)

# Prompt log: seed with some historically plausible prompts
prompts = [
    (f"{months[0].strftime('%Y-%m')}-05", "Create a lead-gen campaign in Rhône-Alpes for TNS insurance", "Assurance", "Google Ads"),
    (f"{months[2].strftime('%Y-%m')}-10", "SME business loan leads in Lyon and Grenoble", "Banque", "Google Ads"),
    (f"{months[5].strftime('%Y-%m')}-17", "Home renovation leads in Auvergne-Rhône-Alpes", "Travaux", "Meta Ads"),
    (f"{months[8].strftime('%Y-%m')}-02", "Real estate buyers in Rhône valley — apartments", "Immobilier", "Google Ads"),
]
head = ['timestamp','user_prompt','category','platform','campaign_id','campaign_name']
with open('campaigns/prompts_log.csv','w',newline='',encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=head)
    w.writeheader()
    # Map prompts to existing campaigns (simple round-robin)
    for i,(ts,prompt,cat,plat) in enumerate(prompts):
        candidates = [c for c in CAMPAIGNS if c['category']==cat and c['platform']==plat]
        if not candidates:
            candidates = [c for c in CAMPAIGNS if c['category']==cat]
        c = candidates[i % len(candidates)]
        w.writerow({
            'timestamp': ts + 'T09:00:00Z',
            'user_prompt': prompt,
            'category': cat,
            'platform': c['platform'],
            'campaign_id': c['campaign_id'],
            'campaign_name': c['campaign_name'],
        })

print('Simulation complete:', months[0].strftime('%Y-%m'), 'to', months[-1].strftime('%Y-%m'))
print(' -> campaigns/simulated_ads.csv')
print(' -> campaigns/prompts_log.csv')
print(' -> campaigns/categories/*.csv')
