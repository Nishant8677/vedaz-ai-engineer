import json
from checker.validator import validate_chat
from checker.duplicates import detect_duplicates
from checker.safety import evaluate_chat_safety
from checker.stats import calculate_stats
from checker.splitter import train_test_split
from utils.io import load_jsonl, save_jsonl, save_json
from utils.config import REPORT_JSON_PATH, TRAIN_DATA_PATH, TEST_DATA_PATH
from utils.logger import get_logger
from tqdm import tqdm

logger = get_logger(__name__)

def run_checker(input_path: str):
    logger.info(f"Loading data from {input_path}")
    raw_chats = load_jsonl(input_path)
    
    if not raw_chats:
        logger.error("No chats found or file does not exist.")
        return

    # 1. Validation
    valid_chats = []
    invalid_count = 0
    for chat in raw_chats:
        if validate_chat(chat):
            valid_chats.append(chat)
        else:
            invalid_count += 1
            
    # 2. Duplicates
    unique_chats, exact_dupes, near_dupes = detect_duplicates(valid_chats)
    
    # 3. Safety
    safe_chats = []
    unsafe_chats = []
    logger.info("Running safety checks (this may take a while due to LLM)...")
    for chat in tqdm(unique_chats, desc="Safety Check"):
        is_safe, reason = evaluate_chat_safety(chat)
        if is_safe:
            safe_chats.append(chat)
        else:
            chat["_safety_reason"] = reason
            unsafe_chats.append(chat)
            
    # 4. Stats
    stats = calculate_stats(safe_chats)
    
    # 5. Split
    train_data, test_data = train_test_split(safe_chats, 0.9)
    save_jsonl(train_data, TRAIN_DATA_PATH)
    save_jsonl(test_data, TEST_DATA_PATH)
    
    # Report
    report = {
        "total_input": len(raw_chats),
        "invalid_schema": invalid_count,
        "exact_duplicates": exact_dupes,
        "near_duplicates": near_dupes,
        "unsafe_chats": len(unsafe_chats),
        "safe_and_valid_chats": len(safe_chats),
        "train_size": len(train_data),
        "test_size": len(test_data),
        "statistics": stats
    }
    
    save_json(report, REPORT_JSON_PATH)
    logger.info(f"Checker finished. Report saved to {REPORT_JSON_PATH}")
    logger.info("Summary:")
    logger.info(f"> Input Chats: {len(raw_chats)}")
    logger.info(f"> Valid Schema: {len(valid_chats)}")
    logger.info(f"> Exact Duplicates: {exact_dupes}")
    logger.info(f"> Near Duplicates: {near_dupes}")
    logger.info(f"> Unsafe: {len(unsafe_chats)}")
    logger.info(f"> Train size: {len(train_data)}")
    logger.info(f"> Test size: {len(test_data)}")
