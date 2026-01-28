import asyncio
import logging
import os
import sqlite3
import requests
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# На хостинге мы достанем ключи из настроек (Environment Variables)
TOKEN = os.getenv("BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_KEY")

logging.basicConfig(level=logging.INFO)

def get_ai_answer(user_message):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    headers = {'Content-Type': 'application/json'}
    prompt = f"Ты Оракул 2026. Ответь мистически и кратко на: {user_message}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "🔮 Звезды сегодня молчат... Попробуй позже."

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("🔮 Оракул запущен на сервере! Спрашивай, смертный.")

@dp.message()
async def any_msg(message: types.Message):
    if message.text:
        await bot.send_chat_action(message.chat.id, "typing")
        loop = asyncio.get_event_loop()
        answer = await loop.run_in_executor(None, get_ai_answer, message.text)
        await message.reply(answer)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
