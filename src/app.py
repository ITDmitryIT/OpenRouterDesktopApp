import flet as ft
from ui.styles import AppStyles
from api.openrouter import get_models, send_message, get_balance
from utils.cache import load_chat_history, save_chat_history
from utils.notifications import send_low_balance
from utils.analytics import update_stats
from utils.logger import setup_logger
import os

class ChatApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.logger = setup_logger()
        self.page.title = "OpenRouter в кармане"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        
        self.models = get_models()
        self.selected_model = self.models[0] if self.models else "openai/gpt-3.5-turbo"
        
        self.chat_history = ft.Column(scroll="auto")
        self.message_input = ft.TextField(hint_text="Введите сообщение...", expand=True)
        self.model_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(m) for m in self.models],
            value=self.selected_model,
            on_change=self.on_model_change
        )
        
        self.balance_text = ft.Text("Баланс: проверка...")
        
        self.build_ui()
        self.load_history()
        self.update_balance()

    def build_ui(self):
        controls_column = ft.Column([
            ft.Row([
                self.message_input,
                ft.IconButton(ft.icons.SEND, on_click=self.send_message)
            ]),
            ft.Row([
                ft.TextButton("Сохранить", on_click=self.save_chat),
                ft.TextButton("Очистить", on_click=self.clear_chat),
                ft.TextButton("Аналитика", on_click=self.show_analytics)
            ])
        ])
        
        model_selection = ft.Column([
            ft.Text("Модель:"),
            self.model_dropdown,
            self.balance_text
        ], **AppStyles.MODEL_SELECTION_COLUMN)
        
        self.page.add(
            ft.Column([
                model_selection,
                self.chat_history,
                controls_column
            ], **AppStyles.MAIN_COLUMN)
        )

    def load_history(self):
        history = load_chat_history()
        for msg in history:
            self.add_message(msg["role"], msg["content"])

    def add_message(self, role: str, content: str):
        bubble = ft.Container(
            content=ft.Text(content),
            **(AppStyles.CHAT_BUBBLE_USER if role == "user" else AppStyles.CHAT_BUBBLE_AI)
        )
        self.chat_history.controls.append(bubble)
        self.page.update()

    def send_message(self, e):
        user_msg = self.message_input.value.strip()
        if not user_msg:
            return
        self.add_message("user", user_msg)
        self.message_input.value = ""
        
        ai_response = send_message(self.selected_model, [
            {"role": "user", "content": user_msg}
        ])
        self.add_message("assistant", ai_response)
        
        save_chat_history([
            {"role": "user", "content": user_msg},
            {"role": "assistant", "content": ai_response}
        ])
        update_stats(self.selected_model)
        self.update_balance()

    def on_model_change(self, e):
        self.selected_model = e.control.value

    def update_balance(self):
        balance = get_balance()
        self.balance_text.value = f"Баланс: ${balance:.2f}"
        if balance < 1.0:
            send_low_balance(balance)
        self.page.update()

    def save_chat(self, e):
        timestamp = __import__("datetime").datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"exports/chat_{timestamp}.json"
        os.makedirs("exports", exist_ok=True)
        save_chat_history([
            {"role": c.content.value, "content": c.content.value} 
            for c in self.chat_history.controls
        ])
        with open(path, "w", encoding="utf-8") as f:
            json.dump([{"role": "user" if "USER" in str(c.bgcolor) else "assistant", "content": c.content.value} 
                      for c in self.chat_history.controls], f, ensure_ascii=False, indent=2)
        self.page.show_snack_bar(ft.SnackBar(ft.Text(f"Чат сохранён: {path}")))

    def clear_chat(self, e):
        self.chat_history.controls.clear()
        save_chat_history([])
        self.page.update()

    def show_analytics(self, e):
        from utils.analytics import update_stats
        stats = update_stats(self.selected_model)
        self.page.show_snack_bar(ft.SnackBar(ft.Text(f"Сессий: {stats['sessions']}")))