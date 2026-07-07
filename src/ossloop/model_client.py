"""Thin wrapper around the local Ollama chat endpoint.

Maker and checker both go through this, but with different system prompts
and different (isolated) context — that separation is what makes the
checker a real check instead of the model grading its own homework.
"""

import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "gpt-oss:20b"


def call_model(system: str, user: str, temperature: float = 0.2) -> str:
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "stream": False,
        "options": {"temperature": temperature},
    }
    resp = requests.post(OLLAMA_URL, json=payload, timeout=300)
    resp.raise_for_status()
    return resp.json()["message"]["content"]
