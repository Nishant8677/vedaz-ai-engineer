import json
from typing import Dict, Any, Optional
from utils.models import Chat
from utils.logger import get_logger

logger = get_logger(__name__)

def parse_generated_json(text: str) -> Optional[Dict[str, Any]]:
    # Remove markdown code fences if present
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
        
    if text.endswith("```"):
        text = text[:-3]
        
    text = text.strip()
    
    try:
        data = json.loads(text)
        # Validate using Pydantic model
        Chat(**data)
        return data
    except Exception as e:
        logger.error(f"Failed to parse or validate generated JSON: {e}")
        return None
