from generator.prompts import TOPICS, GENERATOR_SYSTEM_PROMPT, get_generation_prompt
from generator.retry import generate_with_retry
from utils.io import save_jsonl
from utils.config import GENERATED_DATA_PATH
from utils.logger import get_logger
from tqdm import tqdm

logger = get_logger(__name__)

def run_generator(num_chats: int = 10):
    logger.info(f"Starting generation of {num_chats} chats...")
    generated_chats = []
    
    for i in tqdm(range(num_chats), desc="Generating Chats"):
        topic = TOPICS[i % len(TOPICS)]
        prompt = get_generation_prompt(topic)
        
        chat = generate_with_retry(GENERATOR_SYSTEM_PROMPT, prompt)
        if chat:
            generated_chats.append(chat)
            
    if generated_chats:
        save_jsonl(generated_chats, GENERATED_DATA_PATH)
        logger.info(f"Successfully generated {len(generated_chats)} safe chats.")
        logger.info(f"Saved to {GENERATED_DATA_PATH}")
    else:
        logger.error("Failed to generate any valid chats.")
