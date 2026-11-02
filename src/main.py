import asyncio
import os
from pathlib import Path
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

# Импортируем инициализацию БД из database.py и роутер из handlers.py
from database import init_db
from handlers import router

# НАСТРОЙКА ПУТИ К .ENV (Способ 1)
# __file__ — это путь к текущему файлу main.py
# .parent — папка telegram_bot/
# .parent.parent — корневая папка проекта, где лежит .env
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

# Загружаем переменные окружения из найденного пути
load_dotenv(dotenv_path=ENV_PATH)

TOKEN = os.getenv("BOT_TOKEN")

# Проверка на случай, если токен не считался
if not TOKEN:
    raise ValueError("Ошибка: Токен бота не найден! Проверьте файл .env в корневой директории.")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Подключаем роутер с хэндлерами
dp.include_router(router)

async def main():
    # Инициализируем базу данных при старте
    init_db()
    print("Бот успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

