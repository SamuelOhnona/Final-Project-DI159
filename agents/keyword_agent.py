from __future__ import annotations
from typing import List, Dict
import re

CATEGORY_SEEDS = {
    "Banque": ["bank account", "savings", "loan", "credit", "mortgage"],
    "Assurance": ["insurance", "health insurance", "auto insurance", "home insurance", "liability"],
    "Travaux": ["renovation", "plumber", "electrician", "roof repair", "home improvement"],
    "Immobilier": ["real estate", "apartment for sale", "house for rent", "mortgage broker", "property management"],
}

class KeywordAgent:
    """Generates and scores keywords for the campaign based on the user prompt.
    This version is rule-based for determinism; you can swap with a model later."""
    def __init__(self):
        pass

    @staticmethod
    def _detect_category(prompt: str) -> str:
        p = prompt.lower()
        if any(k in p for k in ["assurance", "insurance"]):
            return "Assurance"
        if any(k in p for k in ["banque", "bank", "loan", "credit"]):
            return "Banque"
        if any(k in p for k in ["travaux", "renovation", "plumber", "electrician"]):
            return "Travaux"
        if any(k in p for k in ["immobilier", "real estate", "apartment", "house"]):
            return "Immobilier"
        return "Assurance"  # default
        
    def propose_keywords(self, prompt: str) -> Dict[str, List[Dict]]:
        category = self._detect_category(prompt)
        base = CATEGORY_SEEDS.get(category, [])
        # derive geo terms
        geo = []
        for token in re.findall(r"[A-Za-zÀ-ÿ\-]+", prompt):
            if token[0].isupper() and len(token) > 3:
                geo.append(token.lower())
        geo = list(dict.fromkeys(geo))  # unique preserve order

        keywords = []
        for seed in base:
            kw = seed
            if geo:
                kw = f"{seed} {' '.join(geo)}"
            score = 60 + (hash(kw) % 40)  # pseudo 'quality' 60..99
            keywords.append({"keyword": kw, "quality_score": score})

        return {"category": category, "keywords": keywords}
