from typing import List, Dict, Any

def calculate_average_metrics(evaluations: List[Dict[str, Any]]) -> Dict[str, float]:
    if not evaluations:
        return {"avg_safety": 0.0, "avg_warmth": 0.0, "avg_honesty": 0.0, "avg_astrology_limits": 0.0, "avg_consistency": 0.0, "avg_overall": 0.0}
        
    total_safety = sum(e.get("safety", 0) for e in evaluations)
    total_warmth = sum(e.get("warmth", 0) for e in evaluations)
    total_honesty = sum(e.get("honesty", 0) for e in evaluations)
    total_astro = sum(e.get("astrology_limits", 0) for e in evaluations)
    total_consistency = sum(e.get("consistency", 0) for e in evaluations)
    total_overall = sum(e.get("overall", 0) for e in evaluations)
    
    n = len(evaluations)
    return {
        "avg_safety": round(total_safety / n, 2),
        "avg_warmth": round(total_warmth / n, 2),
        "avg_honesty": round(total_honesty / n, 2),
        "avg_astrology_limits": round(total_astro / n, 2),
        "avg_consistency": round(total_consistency / n, 2),
        "avg_overall": round(total_overall / n, 2)
    }

def generate_markdown_summary(metrics: Dict[str, float], num_evals: int) -> str:
    md = f"""# Evaluation Summary

**Total Evaluated:** {num_evals}

## Average Scores (out of 5)
- **Overall:** {metrics['avg_overall']}
- **Safety:** {metrics['avg_safety']}
- **Warmth:** {metrics['avg_warmth']}
- **Honesty:** {metrics['avg_honesty']}
- **Astrology Limits:** {metrics['avg_astrology_limits']}
- **Consistency:** {metrics['avg_consistency']}

*Note: Scores are determined by Gemini Cross-Model Evaluation.*
"""
    return md
