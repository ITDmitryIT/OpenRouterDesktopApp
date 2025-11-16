import os
import telebot
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = telebot.TeleBot(BOT_TOKEN) if BOT_TOKEN and CHAT_ID else None

def send_low_balance(balance: float):
    if not bot:
        return
    message = f"Низкий баланс OpenRouter!\nТекущий баланс: ${balance:.2f}\nПополните счёт!"
    try:
        bot.send_message(CHAT_ID, message)
    except Exception as e:
        print(f"Ошибка Telegram: {e}")