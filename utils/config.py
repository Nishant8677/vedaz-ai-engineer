import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)

# File paths
ORIGINAL_DATA_PATH = DATA_DIR / "original.jsonl"
TRAIN_DATA_PATH = DATA_DIR / "train.jsonl"
TEST_DATA_PATH = DATA_DIR / "test.jsonl"
GENERATED_DATA_PATH = DATA_DIR / "generated.jsonl"
REPORT_JSON_PATH = DATA_DIR / "checker_report.json"
EVAL_CSV_PATH = DATA_DIR / "evaluation.csv"
EVAL_MD_PATH = DATA_DIR / "evaluation_summary.md"

# Model constants
DEFAULT_MODEL = "deepseek-ai/DeepSeek-V3"
