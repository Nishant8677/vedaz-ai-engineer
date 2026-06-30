import json
import csv
from pathlib import Path
from typing import List, Dict, Any

def load_jsonl(file_path: str | Path) -> List[Dict[str, Any]]:
    """Load a JSONL file into a list of dictionaries."""
    data = []
    path = Path(file_path)
    if not path.exists():
        return data
    
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    return data

def save_jsonl(data: List[Dict[str, Any]], file_path: str | Path) -> None:
    """Save a list of dictionaries to a JSONL file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

def save_json(data: Dict[str, Any], file_path: str | Path) -> None:
    """Save a dictionary to a JSON file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def save_csv(data: List[Dict[str, Any]], file_path: str | Path, fieldnames: List[str]) -> None:
    """Save a list of dictionaries to a CSV file."""
    if not data:
        return
    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
