import random
from typing import List, Dict, Any, Tuple

def train_test_split(chats: List[Dict[str, Any]], train_ratio: float = 0.9) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    # Shuffle for randomness
    shuffled = chats.copy()
    random.shuffle(shuffled)
    
    split_index = int(len(shuffled) * train_ratio)
    train_data = shuffled[:split_index]
    test_data = shuffled[split_index:]
    
    return train_data, test_data
