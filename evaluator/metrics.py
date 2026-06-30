from typing import List, Dict, Any

def calculate_average_metrics(evaluations: List[Dict[str, Any]]) -> Dict[str, float]:
    if not evaluations:
        return {"avg_safety": 0.0, "avg_warmth": 0.0, "avg_honesty": 0.0}
        
    total_safety = sum(e.get("safety", 0) for e in evaluations)
    total_warmth = sum(e.get("warmth", 0) for e in evaluations)
    total_honesty = sum(e.get("honesty", 0) for e in evaluations)
    
    n = len(evaluations)
    return {
        "avg_safety": round(total_safety / n, 2),
        "avg_warmth": round(total_warmth / n, 2),
        "avg_honesty": round(total_honesty / n, 2)
    }

def generate_markdown_summary(metrics: Dict[str, float], num_evals: int) -> str:
    md = f"""# Evaluation Summary

**Total Evaluated:** {num_evals}

## Average Scores (out of 5)
- **Safety:** {metrics['avg_safety']}
- **Warmth:** {metrics['avg_warmth']}
- **Honesty:** {metrics['avg_honesty']}

*Note: Scores are determined by an LLM-as-a-Judge.*
"""
    return md
