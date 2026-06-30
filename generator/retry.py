from typing import Dict, Any, Optional
from generator.parser import parse_generated_json
from checker.safety import evaluate_chat_safety
from utils.llm import generate_text
from utils.logger import get_logger

logger = get_logger(__name__)

def generate_with_retry(system_prompt: str, user_prompt: str, max_retries: int = 3) -> Optional[Dict[str, Any]]:
    current_user_prompt = user_prompt
    
    for attempt in range(1, max_retries + 1):
        logger.debug(f"Generation attempt {attempt}/{max_retries}")
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": current_user_prompt}
        ]
        
        response_text = generate_text(messages, json_mode=True)
        if not response_text:
            continue
            
        chat_data = parse_generated_json(response_text)
        if not chat_data:
            current_user_prompt = f"{user_prompt}\n\nWARNING: Your previous response was invalid JSON or violated schema. Please fix it."
            continue
            
        # Run through safety checker
        is_safe, reason = evaluate_chat_safety(chat_data)
        if is_safe:
            return chat_data
        else:
            logger.warning(f"Generated chat was unsafe: {reason}. Retrying...")
            current_user_prompt = f"{user_prompt}\n\nWARNING: Your previous response was flagged as UNSAFE because: {reason}. Rewrite it to be safe."
            
    logger.error("Max retries reached. Failed to generate a safe/valid chat.")
    return None
