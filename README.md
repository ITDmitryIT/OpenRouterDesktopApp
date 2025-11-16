# OpenRouter в кармане — Десктоп + Мобильное приложение

AI-чат с OpenRouter.ai  
Аутентификация по PIN  
Уведомления в Telegram  
Сохранение чата  
Сборка в APK

---

## Функции

- Вход по API-ключу → генерация 4-значного PIN
- Повторный вход по PIN
- Уведомления о низком балансе в Telegram
- Сохранение чата в JSON
- Выбор модели ИИ
- Логирование и аналитика
- Поддержка Android (APK)

---

## Установка

```bash
git clone https://github.com/ВАШ_НИК/OpenRouterDesktopApp.git
cd OpenRouterDesktopApp
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

##  Запуск

```bash
python src/main.py

## Сборка APK
```bash
flet build apk --project-name "AIChat" --package-name "com.example.aichat" --icon "assets/icon.png"

## .env (пример)

OPENROUTER_API_KEY=sk-or-v1-...
TELEGRAM_BOT_TOKEN=123456:ABCDEF...
TELEGRAM_CHAT_ID=123456789
