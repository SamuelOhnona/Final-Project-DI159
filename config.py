import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

def get_openai_api_key() -> Optional[str]:
    return os.getenv("OPENAI_API_KEY")

def get_openai_client():
    """Return an OpenAI client if API key is present, else None.
    Agents should handle None (mock mode)."""
    api_key = get_openai_api_key()
    if not api_key:
        return None
    try:
        import openai
        openai.api_key = api_key
        return openai
    except Exception:
        return None
