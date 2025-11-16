import shelve
import json
import os
from datetime import datetime

CACHE_DB = "cache/auth.db"
HISTORY_FILE = "cache/history.json"

os.makedirs("cache", exist_ok=True)
os.makedirs("exports", exist_ok=True)

def save_auth(api_key: str):
    pin = str(__import__("random").randint(1000, 9999))
    with shelve.open(CACHE_DB) as db:
        db["api_key"] = api_key
        db["pin"] = pin
    return pin

def get_auth():
    try:
        with shelve.open(CACHE_DB) as db:
            return db.get("api_key"), db.get("pin")
    except:
        return None, None

def reset_auth():
    if os.path.exists(CACHE_DB):
        os.remove(CACHE_DB)
    if os.path.exists(CACHE_DB + ".db"):
        os.remove(CACHE_DB + ".db")

def save_chat_history(messages: list):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

def load_chat_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []