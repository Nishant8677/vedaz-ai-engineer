import os
import json
from openai import OpenAI
from google import genai
from typing import Optional, Dict, Any, List
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from utils.config import OPENROUTER_API_KEY, GEMINI_API_KEY, DEFAULT_MODEL
from utils.logger import get_logger

logger = get_logger(__name__)

client = None
if OPENROUTER_API_KEY:
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
        )
    except Exception as e:
        logger.error(f"Failed to initialize OpenRouter client: {e}")

gemini_client = None
if GEMINI_API_KEY:
    try:
        gemini_client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception as e:
        logger.error(f"Failed to initialize Gemini client: {e}")

@retry(
    wait=wait_exponential(multiplier=1, min=2, max=10),
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type(Exception),
    reraise=False
)
def generate_text(messages: List[Dict[str, str]], model: str = DEFAULT_MODEL, max_tokens: int = 1024, temperature: float = 0.7, json_mode: bool = False) -> Optional[str]:
    """Generate text using OpenRouter API."""
    if not client:
        logger.error("OpenRouter API client is not initialized. Check your OPENROUTER_API_KEY.")
        return None
        
    try:
        kwargs = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "extra_headers": {
                "HTTP-Referer": "https://github.com/vedaz-ai-engineer",
                "X-Title": "Vedaz AI Engineer",
            }
        }
        
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
            
        response = client.chat.completions.create(**kwargs)
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error calling OpenRouter API: {e}")
        raise e  # Reraise to trigger tenacity retry

@retry(
    wait=wait_exponential(multiplier=1, min=2, max=10),
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type(Exception),
    reraise=False
)
def generate_with_gemini(prompt: str, json_mode: bool = False) -> Optional[str]:
    """Generate text using Gemini 2.5 Flash."""
    if not gemini_client:
        logger.error("Gemini API client is not initialized. Check your GEMINI_API_KEY.")
        return None
        
    try:
        from google.genai import types
        
        config = types.GenerateContentConfig(
            temperature=0.7,
        )
        if json_mode:
            config.response_mime_type = "application/json"
            
        response = gemini_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=config,
        )
        return response.text
    except Exception as e:
        logger.error(f"Error calling Gemini API: {e}")
        raise e  # Reraise to trigger tenacity retry
