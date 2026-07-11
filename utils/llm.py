import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("HF_API_KEY")
MODEL = os.getenv("HF_MODEL", "Qwen/Qwen3-32B")

API_URL = "https://router.huggingface.co/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


def ask_llm(prompt: str) -> str:

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a helpful AI assistant. "
                    "Never output <think> tags or your reasoning. "
                    "Return ONLY the final answer."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)
    response.raise_for_status()

    data = response.json()

    answer = data["choices"][0]["message"]["content"]

    # Remove <think>...</think> if it exists
    answer = re.sub(
        r"<think>.*?</think>",
        "",
        answer,
        flags=re.DOTALL | re.IGNORECASE
    ).strip()

    return answer