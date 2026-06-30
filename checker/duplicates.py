import hashlib
from typing import List, Dict, Any, Tuple
from rapidfuzz import fuzz

def _get_chat_text(chat: Dict[str, Any]) -> str:
    """Concatenate all message contents for comparison."""
    return " ".join([m.get("content", "") for m in chat.get("messages", [])])

def detect_duplicates(chats: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], int, int]:
    """
    Returns (unique_chats, exact_dupes_count, near_dupes_count)
    """
    unique_chats = []
    exact_dupes = 0
    near_dupes = 0
    
    seen_hashes = set()
    
    for chat in chats:
        text = _get_chat_text(chat)
        chat_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
        
        # Exact duplicate
        if chat_hash in seen_hashes:
            exact_dupes += 1
            continue
            
        # Near duplicate
        is_near_dupe = False
        for unique_chat in unique_chats:
            unique_text = _get_chat_text(unique_chat)
            similarity = fuzz.ratio(text, unique_text)
            if similarity >= 90:
                is_near_dupe = True
                break
                
        if is_near_dupe:
            near_dupes += 1
            continue
            
        seen_hashes.add(chat_hash)
        unique_chats.append(chat)
        
    return unique_chats, exact_dupes, near_dupes
