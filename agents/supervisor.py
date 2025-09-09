from __future__ import annotations
from typing import Dict, Any, List
import csv, os, uuid, datetime
from .keyword_agent import KeywordAgent
from .creative_agent import CreativeAgent
from .bid_manager import BidManagerAgent

PROMPTS_LOG = os.path.join("campaigns", "prompts_log.csv")

class SupervisorAgent:
    """Entry point: receives a campaign brief and coordinates other agents.
    Also persists the prompt to prompts_log.csv with a campaign_id."""
    def __init__(self):
        self.keyword_agent = KeywordAgent()
        self.creative_agent = CreativeAgent()
        self.bid_agent = BidManagerAgent()
        os.makedirs("campaigns", exist_ok=True)

    def submit_prompt(self, user_prompt: str, platform: str = "Google Ads") -> Dict[str, Any]:
        kw_result = self.keyword_agent.propose_keywords(user_prompt)
        category = kw_result["category"]
        campaign_id = str(uuid.uuid4())[:8]
        campaign_name = f"{category} - {platform} - {campaign_id}"

        # Persist prompt
        self._append_prompt_log({
            "timestamp": datetime.datetime.utcnow().isoformat(timespec="seconds"),
            "user_prompt": user_prompt,
            "category": category,
            "platform": platform,
            "campaign_id": campaign_id,
            "campaign_name": campaign_name,
        })

        ad_copy = self.creative_agent.generate_ad_copy(user_prompt)
        img_prompt = self.creative_agent.generate_image_prompt(user_prompt)

        result = {
            "campaign_id": campaign_id,
            "campaign_name": campaign_name,
            "category": category,
            "platform": platform,
            "keywords": kw_result["keywords"],
            "ad_copy": ad_copy,
            "image_prompt": img_prompt,
        }
        return result

    def _append_prompt_log(self, row: Dict[str, str]):
        head = ["timestamp", "user_prompt", "category", "platform", "campaign_id", "campaign_name"]
        write_header = not os.path.exists(PROMPTS_LOG)
        with open(PROMPTS_LOG, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=head)
            if write_header:
                w.writeheader()
            w.writerow(row)
