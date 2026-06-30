from evaluator.judge import evaluate_answer
from evaluator.metrics import calculate_average_metrics, generate_markdown_summary
from utils.llm import generate_text
from utils.io import save_csv, load_jsonl
from utils.config import EVAL_CSV_PATH, EVAL_MD_PATH, TEST_QUESTIONS_PATH
from utils.logger import get_logger
from tqdm import tqdm

logger = get_logger(__name__)

def run_evaluator():
    logger.info("Starting Quality Evaluation...")
    results = []
    
    try:
        raw_questions = load_jsonl(TEST_QUESTIONS_PATH)
        questions = [q["question"] for q in raw_questions if "question" in q]
    except Exception as e:
        logger.error(f"Failed to load test questions: {e}")
        return
        
    for question in tqdm(questions, desc="Evaluating"):
        # 1. Generate answer from "Vedaz"
        system_prompt = "You are Vedaz, a helpful and honest AI astrologer."
        answer = generate_text([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ])
        
        if not answer:
            logger.warning(f"Failed to generate answer for: {question}")
            continue
            
        # 2. Judge the answer
        judge_res = evaluate_answer(question, answer)
        if not judge_res:
            logger.warning(f"Failed to judge answer for: {question}")
            continue
            
        results.append({
            "question": question,
            "answer": answer,
            "safety": judge_res.safety,
            "warmth": judge_res.warmth,
            "honesty": judge_res.honesty,
            "astrology_limits": judge_res.astrology_limits,
            "consistency": judge_res.consistency,
            "overall": judge_res.overall,
            "strengths": judge_res.strengths,
            "weaknesses": judge_res.weaknesses,
            "reasoning": judge_res.reasoning
        })
        
        # Simple results table output as requested
        print(f"Q: {question[:30]}... | Safety: {judge_res.safety} | Warmth: {judge_res.warmth} | Honesty: {judge_res.honesty} | Overall: {judge_res.overall}")
        
    if not results:
        logger.error("No evaluations completed successfully.")
        return
        
    # Metrics
    metrics = calculate_average_metrics(results)
    
    # Export CSV
    save_csv(results, EVAL_CSV_PATH, ["question", "answer", "safety", "warmth", "honesty", "astrology_limits", "consistency", "overall", "strengths", "weaknesses", "reasoning"])
    
    # Export MD
    md_content = generate_markdown_summary(metrics, len(results))
    with open(EVAL_MD_PATH, "w", encoding="utf-8") as f:
        f.write(md_content)
        
    logger.info(f"Evaluation complete. Saved to {EVAL_CSV_PATH} and {EVAL_MD_PATH}")
    logger.info(f"Average Scores: Overall={metrics['avg_overall']}, Safety={metrics['avg_safety']}, Warmth={metrics['avg_warmth']}, Honesty={metrics['avg_honesty']}")
