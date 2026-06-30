from typing import List, Dict, Any

def calculate_stats(valid_chats: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not valid_chats:
        return {}

    num_chats = len(valid_chats)
    total_turns = 0
    total_words = 0
    longest_chat_words = 0
    shortest_chat_words = float('inf')
    total_assistant_words = 0
    total_user_words = 0
    assistant_msgs_count = 0
    user_msgs_count = 0

    for chat in valid_chats:
        messages = chat.get("messages", [])
        turns = len(messages)
        total_turns += turns
        
        chat_words = 0
        for msg in messages:
            words = len(msg.get("content", "").split())
            chat_words += words
            
            if msg.get("role") == "assistant":
                total_assistant_words += words
                assistant_msgs_count += 1
            elif msg.get("role") == "user":
                total_user_words += words
                user_msgs_count += 1
                
        total_words += chat_words
        longest_chat_words = max(longest_chat_words, chat_words)
        shortest_chat_words = min(shortest_chat_words, chat_words)

    if shortest_chat_words == float('inf'):
        shortest_chat_words = 0

    return {
        "num_chats": num_chats,
        "avg_turns": round(total_turns / num_chats, 2),
        "avg_words_per_chat": round(total_words / num_chats, 2),
        "longest_chat_words": longest_chat_words,
        "shortest_chat_words": shortest_chat_words,
        "avg_assistant_words": round(total_assistant_words / max(1, assistant_msgs_count), 2),
        "avg_user_words": round(total_user_words / max(1, user_msgs_count), 2)
    }
