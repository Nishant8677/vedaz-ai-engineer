import os
import json
from together import Together
from typing import Optional, Dict, Any, List
from utils.config import TOGETHER_API_KEY, DEFAULT_MODEL
from utils.logger import get_logger

logger = get_logger(__name__)

client = None
if TOGETHER_API_KEY:
    try:
        client = Together(api_key=TOGETHER_API_KEY)
    except Exception as e:
        logger.error(f"Failed to initialize Together client: {e}")

def generate_text(messages: List[Dict[str, str]], model: str = DEFAULT_MODEL, max_tokens: int = 1024, temperature: float = 0.7, json_mode: bool = False) -> Optional[str]:
    """Generate text using Together API."""
    if not client:
        logger.error("Together API client is not initialized. Check your TOGETHER_API_KEY.")
        return None
        
    try:
        kwargs = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
            
        response = client.chat.completions.create(**kwargs)
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error calling Together API: {e}")
        return None
