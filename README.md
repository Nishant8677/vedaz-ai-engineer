# Vedaz AI Engineer Pipeline

A production-quality LLM Dataset Engineering Pipeline that validates, generates, filters, and evaluates conversational AI datasets.

## Overview

This project provides tools to:
- Check and validate dataset schemas.
- Detect exact and near-duplicate conversations.
- Automatically flag unsafe content via Regex and LLM-as-a-judge.
- Generate new safe conversations using Together AI.
- Evaluate model responses based on Safety, Warmth, and Honesty.

## Architecture

```text
                    Original Dataset (.jsonl)
                           │
                           ▼
                      Chat Checker
                 ┌─────────┴─────────┐
                 │                   │
            Regex Rules         Gemini Judge
                 │                   │
                 └─────────┬─────────┘
                           │
                     Checker Report
                           │
                           ▼
                    Chat Generator
                           │
               OpenRouter (Generator)
              DeepSeek / Qwen / Llama
                           │
                           ▼
                  Generated Chats
                           │
                           ▼
                   Run Checker Again
                           │
                   PASS ─────────── FAIL
                    │                 │
                    ▼                 ▼
             generated.jsonl      Regenerate
                    │
                    ▼
                  Quality Evaluation
                           │
                    Gemini Judge
                           │
                           ▼
                  evaluation.csv
```

## Installation

1. Create a virtual environment and install dependencies:
```bash
python -m venv .venv
# Activate the venv (Windows: .venv\Scripts\activate | Unix: source .venv/bin/activate)
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and add your OpenRouter API and Gemini API keys:
```bash
OPENROUTER_API_KEY=your_openrouter_key_here
GEMINI_API_KEY=your_gemini_key_here
```

## Usage

### 1. Check Dataset
```bash
python main.py check
```
This validates the dataset, checks for duplicates, flags unsafe content, splits train/test, and produces `checker_report.json`.

### 2. Generate Chats
```bash
python main.py generate
```
This uses OpenRouter to generate new simulated chats and automatically filters out any that fail safety or schema checks, saving valid ones to `generated.jsonl`.

### 3. Evaluate Responses
```bash
python main.py evaluate
```
This runs a set of test questions against the assistant and uses an LLM judge to score them on Safety, Warmth, and Honesty. Results are saved in `evaluation.csv` and `evaluation_summary.md`.

## Design Decisions

- **Provider-Agnostic Generation:** The generation pipeline is provider-agnostic. By abstracting generation behind OpenRouter, different open-weight models (like DeepSeek, Llama 3.3, or Qwen) can be evaluated simply by changing the `DEFAULT_MODEL` variable, without modifying the rest of the system.
- **Cross-Model Evaluation:** We use OpenRouter to generate the responses, but we use Gemini 2.5 Flash as the evaluator and safety checker. This eliminates the self-evaluation bias that happens when a model family rates its own outputs.
- **Why RapidFuzz?** For dataset sizes typical in this assignment (15-30 chats), RapidFuzz is highly effective, lightweight, and doesn't require downloading large sentence embedding models.
- **Why Hybrid Safety?** Regex handles explicit violations instantly, while the Gemini LLM judge catches nuanced or context-dependent violations (like hallucinating planetary positions).
- **Why Pydantic?** Enforces strict schema typing universally across all modules, drastically reducing downstream parsing errors.
- **Why reuse the checker?** Running generated chats through the exact same checker ensures our synthetic data meets the exact same quality standard as human data.

## Limitations

- **Regex Limitations:** Rule-based regex can miss subtle violations or variations in spelling.
- **LLM Judge Variability:** LLM judgments can sometimes be inconsistent between runs.
- **RapidFuzz vs Semantic:** RapidFuzz detects lexical similarity but might miss semantic duplicates (different words, same meaning). For large datasets, a transition to SentenceTransformers would be necessary.
- **Dataset Size:** The pipeline works wonderfully for smaller datasets but might need batching logic or parallelization for processing tens of thousands of rows.
