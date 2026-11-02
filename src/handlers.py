from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from database import get_topic_description
from keyboard import get_catalog_keyboard, get_back_keyboard, get_start_keyboard

router = Router()

@router.message(Command("start"))
async def start_command(message:Message):
    await message.answer("Welcome! Please choose an option:", reply_markup=get_start_keyboard())

@router.message(F.text == "Каталог")
async def catalog_command(message:Message):
    await message.answer("Выберите тему:", reply_markup=get_catalog_keyboard())

@router.callback_query(F.data.startswith("topic_"))
async def callback_query_handler(callback_query: CallbackQuery):
    await callback_query.answer()

    topic_code = callback_query.data.replace("topic_", "")

    description = get_topic_description(topic_code)

    await callback_query.message.edit_text(
            text=description,
            reply_markup=get_back_keyboard()
    )

@router.callback_query(F.data == "back_to_catalog")
async def back_to_catalog_command(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text("Выберите тему:", reply_markup=get_catalog_keyboard())
