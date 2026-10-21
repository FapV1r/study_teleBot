import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command(commands=["start"]))
async def start(message: Message):
    await message.answer("Hello! I am your bot. How can I assist you today?")

@dp.message(Command(commands=["help"]))
async def help_command(message: Message):
    await message.answer("Here are the commands you can use:\n/start - Start the bot\n/help - Show this help message")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())