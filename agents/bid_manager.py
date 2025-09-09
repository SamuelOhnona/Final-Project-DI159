from __future__ import annotations
from typing import List, Dict

class BidManagerAgent:
    """Suggests bid multipliers and budget allocation per campaign.
    This mock strategy uses keyword quality to bias spend."""
    def recommend(self, campaigns: List[Dict]) -> Dict[str, float]:
        # campaigns: list of {campaign_id, avg_quality}
        total = sum(c.get("avg_quality", 70) for c in campaigns) or 1.0
        allocation = {}
        for c in campaigns:
            w = c.get("avg_quality", 70) / total
            allocation[c["campaign_id"]] = round(w, 4)
        return allocation
