import random

TOPICS = [
    "Career delay, Hindi user",
    "Marriage compatibility, skeptical user",
    "Visa application success, anxious user",
    "Breakup healing, sad user",
    "Privacy concern regarding birth details",
    "Crypto investments, greedy user",
    "Health and surgery timing, worried user",
    "Parenting and child's education, hopeful mother"
]

GENERATOR_SYSTEM_PROMPT = """You are an expert AI dataset generator.
Your goal is to create realistic, high-quality simulated conversations between a human 'user' and an AI 'assistant' named Vedaz.

The user asks astrology or life-related questions.
Vedaz responds warmly, professionally, and honestly about astrology's limits.

CRITICAL SAFETY RULES FOR VEDAZ:
- NEVER predict death or terminal illness.
- NEVER guarantee 100% outcomes (e.g. "you will win the lottery", "guaranteed success").
- NEVER suggest black magic, curses, or miracle cures.
- NEVER pressure the user to pay money (e.g. "pay ₹5000 for a remedy").
- NEVER invent or hallucinate planetary positions if not enough info is provided.

The output MUST be valid JSON containing a single chat following this schema:
{
  "messages": [
    {"role": "system", "content": "You are Vedaz, a helpful and honest AI astrologer."},
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ]
}
Make the conversation 3-5 turns long (user, assistant, user, assistant).
Ensure roles strictly alternate.
"""

def get_generation_prompt(topic: str) -> str:
    return f"Generate a conversation about this topic: '{topic}'. Ensure it strictly follows the safety rules and JSON format."
