from __future__ import annotations
from typing import Dict, Any, Optional
from config import get_openai_client

class CreativeAgent:
    """Generates ad copy (and optionally image prompts).
    Uses OpenAI if key is present; otherwise returns deterministic mock."""
    def __init__(self):
        self.client = get_openai_client()

    def generate_ad_copy(self, brief: str, max_tokens: int = 120) -> str:
        system = "You are a concise, persuasive marketing copywriter. Return 2-3 short ad lines."
        if self.client is None:
            return ("Save time & money today. Get your personalized offer.\n"
                    "Fast approval. Trusted by professionals in your area.")
        try:
            resp = self.client.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": brief},
                ],
                max_tokens=max_tokens,
                temperature=0.7,
            )
            return resp["choices"][0]["message"]["content"].strip()
        except Exception:
            # Fallback
            return ("Optimize your budget. High-intent leads delivered.\n"
                    "Get started now — limited-time offer.")

    def generate_image_prompt(self, brief: str) -> str:
        return f"Minimal, professional display banner illustrating: {brief}. Clean layout, bold headline, clear CTA."
