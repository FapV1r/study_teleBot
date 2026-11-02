from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from database import get_topics_from_db

def get_catalog_keyboard():
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

def get_start_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Каталог"))
    builder.add(KeyboardButton(text="Помощь"))
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

