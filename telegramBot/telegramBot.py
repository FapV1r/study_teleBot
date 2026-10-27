import asyncio
import os
import sqlite3

from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()
router = Router()

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_router(router)

DB_NAME = "bot_database.db"


# === БЛОК РАБОТЫ С БАЗОЙ ДАННЫХ ===

def init_db():
    """Создает таблицу и заполняет её базовыми темами, если базы еще нет"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE,
            title TEXT,
            description TEXT
        )
    """)
    
    default_topics = [
        (
            "data_types", 
            "Типы данных", 
            "Типы данных в C++ включают:\n- int (целые числа)\n- float (числа с плавающей точкой)\n- char (символы)\n- bool (логические значения)\n- long (длинные целые числа)\n- double (числа с двойной точностью)\n- string (строки)"
        ),
        (
            "conditional_operators", 
            "Условные операторы", 
            "Условные операторы в C++ включают:\n- if (если)\n- else (иначе)\n- else if (иначе если)\n- switch (выбор)"
        ),
        (
            "loops", 
            "Циклы", 
            "Циклы в C++ включают:\n- for (для)\n- while (пока)\n- do-while (сделай-пока)"
        )
    ]
    
    cursor.execute("SELECT COUNT(*) FROM topics")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO topics (code, title, description) VALUES (?, ?, ?)", default_topics)
        conn.commit()
        
    conn.close()


def get_topics_from_db():
    """Получает список всех доступных тем для построения меню"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT code, title FROM topics")
    topics = cursor.fetchall()
    conn.close()
    return topics


def get_topic_description(topic_code):
    """Получает описание конкретной темы по её коду"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT description FROM topics WHERE code = ?", (topic_code,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else "Тема не найдена."


# === БЛОК КЛАВИАТУР ===

def get_catalog_keyboard():
    """Динамически строит клавиатуру на основе записей в базе данных"""
    builder = InlineKeyboardBuilder()
    topics = get_topics_from_db()
    
    for code, title in topics:
        builder.add(InlineKeyboardButton(text=title, callback_data=f"topic_{code}"))
        
    builder.adjust(2)
    return builder.as_markup()


def get_back_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="⬅️ Назад в каталог", callback_data="back_to_catalog"))
    return builder.as_markup()


# === БЛОК ХЭНДЛЕРОВ ===

@router.message(Command("start"))
async def start_command(message: Message):
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Каталог"))
    builder.add(KeyboardButton(text="Помощь"))
    markup = builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    await message.answer("Welcome! Please choose an option:", reply_markup=markup)


@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer("Here are the commands you can use:\n/start - Start the bot\n/help - Show this help message")


@router.message(F.text == 'Каталог')
async def catalog_command(message: Message):
    await message.answer("Выберите тему: ", reply_markup=get_catalog_keyboard())


@router.message(F.text == 'Помощь')
async def help_text_command(message: Message):
    await help_command(message)


@router.callback_query(F.data.startswith("topic_"))
async def callback_query_topic_handler(callback_query: CallbackQuery):
    await callback_query.answer()
    
    # Отрезаем префикс "topic_", чтобы получить чистый код темы (например, "loops")
    topic_code = callback_query.data.split("_", 1)[1]
    
    # Достаем текст из БД
    description = get_topic_description(topic_code)
    
    # Редактируем сообщение
    await callback_query.message.edit_text(
        text=description,
        reply_markup=get_back_keyboard()
    )


@router.callback_query(F.data == "back_to_catalog")
async def back_to_catalog_command(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text("Выберите тему: ", reply_markup=get_catalog_keyboard())


# === ЗАПУСК ===

async def main():
    # Инициализируем базу данных перед стартом опроса сервера
    init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
