import flet as ft
import requests
from utils.cache import save_auth, get_auth, reset_auth
from api.openrouter import get_balance

class LoginWindow:
    def __init__(self, page: ft.Page, on_success):
        self.page = page
        self.on_success = on_success
        self.api_key_field = ft.TextField(label="API Key OpenRouter", password=True)
        self.pin_field = ft.TextField(label="PIN (4 цифры)", password=True, max_length=4)
        self.error_text = ft.Text("", color=ft.Colors.RED)  # ИСПРАВЛЕНО
        self.key, self.pin = get_auth()
        
        if not self.key:
            self.show_key_input()
        else:
            self.show_pin_input()
            
    def show_key_input(self):
        def validate(e):
            key = self.api_key_field.value.strip()
            if not key:
                self.error_text.value = "Введите ключ!"
                self.page.update()
                return
            
            try:
                balance = get_balance()
                if balance > 0:
                    pin = save_auth(key)
                    self.error_text.value = f"Ключ сохранён! Ваш PIN: {pin}"
                    self.page.update()
                    self.page.dialog = None
                    self.on_success()
                else:
                    self.error_text.value = "Баланс нулевой!"
            except:
                self.error_text.value = "Ошибка проверки ключа."
            self.page.update()

        self.page.add(
            ft.Column([
                ft.Text("Вход по API ключу", size=20, weight="bold"),
                self.api_key_field,
                ft.ElevatedButton("Проверить", on_click=validate),
                self.error_text
            ], horizontal_alignment="center")
        )

    def show_pin_input(self):
        def check(e):
            if self.pin_field.value == self.pin:
                self.page.dialog = None
                self.on_success()
            else:
                self.error_text.value = "Неверный PIN!"
                self.page.update()

        def reset(e):
            reset_auth()
            self.page.clean()
            LoginWindow(self.page, self.on_success)

        self.page.add(
            ft.Column([
                ft.Text("Вход по PIN", size=20, weight="bold"),
                self.pin_field,
                ft.Row([
                    ft.ElevatedButton("Войти", on_click=check),
                    ft.TextButton("Сбросить ключ", on_click=reset)
                ], alignment="center"),
                self.error_text
            ], horizontal_alignment="center")
        )