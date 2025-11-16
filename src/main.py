import flet as ft
from app import ChatApp
from ui.components import LoginWindow
from utils.cache import get_auth  # ДОБАВЛЕНО!

def main(page: ft.Page):
    def start_app():
        ChatApp(page)
    
    api_key, _ = get_auth()  # Теперь работает!
    if not api_key:
        LoginWindow(page, start_app)
    else:
        start_app()

if __name__ == "__main__":
    ft.app(target=main)

    