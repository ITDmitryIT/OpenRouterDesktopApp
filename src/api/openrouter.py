import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_BASE = "https://openrouter.ai/api/v1"
API_KEY = os.getenv("OPENROUTER_API_KEY")

def get_models():
    headers = {"Authorization": f"Bearer {API_KEY}"}
    try:
        response = requests.get(f"{API_BASE}/models", headers=headers)
        response.raise_for_status()
        return [model["id"] for model in response.json()["data"]]
    except Exception as e:
        print(f"Ошибка получения моделей: {e}")
        return []

def get_balance():
    headers = {"Authorization": f"Bearer {API_KEY}"}
    try:
        response = requests.get(f"{API_BASE}/auth/me", headers=headers)
        if response.status_code == 200:
            return response.json().get("balance", 0.0)
        return 0.0
    except:
        return 0.0

def send_message(model: str, messages: list):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": messages
    }
    try:
        response = requests.post(f"{API_BASE}/chat/completions", json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Ошибка API: {e}"