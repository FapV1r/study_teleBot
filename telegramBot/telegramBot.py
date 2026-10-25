import asyncio
import os

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
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Типы данных", callback_data="data_types"))
    builder.add(InlineKeyboardButton(text="Условные операторы", callback_data="conditional_operators"))
    builder.add(InlineKeyboardButton(text="Циклы", callback_data="loops"))
    builder.adjust(2)
    await message.answer("Выберите тему: ", reply_markup=builder.as_markup())

@router.message(F.text == 'Помощь')
async def help_text_command(message: Message):
    await help_command(message)

@router.callback_query(F.data == "data_types")
async def callback_query_data_types_command(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer(
        "Типы данных в C++ включают:\n"
        "- int (целые числа)\n"
        "- float (числа с плавающей точкой)\n"
        "- char (символы)\n"
        "- bool (логические значения)\n"
        "- long (длинные целые числа)\n"
        "- double (числа с двойной точностью)\n"
        "- string (строки)"
    )

@router.callback_query(F.data == "conditional_operators")
async def callback_query_conditional_operators_command(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer(
        "Условные операторы в C++ включают:\n"
        "- if (если)\n"
        "- else (иначе)\n"
        "- else if (иначе если)\n"
        "- switch (выбор)"
    )

@router.callback_query(F.data == "loops")
async def callback_query_loops_command(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer(
        "Циклы в C++ включают:\n"
        "- for (для)\n"
        "- while (пока)\n"
        "- do-while (сделай-пока)"
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
