from pydantic import ValidationError
from typing import Dict, Any
from utils.models import Chat
from utils.logger import get_logger

logger = get_logger(__name__)

def validate_chat(chat_data: Dict[str, Any]) -> bool:
    """Validate a chat dictionary against the Chat Pydantic model."""
    try:
        Chat(**chat_data)
        return True
    except ValidationError as e:
        logger.debug(f"Validation failed: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during validation: {e}")
        return False
