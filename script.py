import asyncio
from datetime import datetime

import requests
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message

BOT_TOKEN = "8978587158:AAGQGHazMpzmAzh6OIAKp9S6CEOVSKRgk5Y"
OPENROUTER_API_KEY = "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"


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()



@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "👋 Привет!\n\n"
        "Я AI Telegram бот.\n"
        "Напиши любой вопрос."
    )

# =========================
# AI CHAT
# =========================

@dp.message(F.text)
async def chat(message: Message):

    user_text = message.text

    wait_message = await message.answer("🤖 Думаю...")

    try:

        # Текущая дата
        current_date = datetime.now().strftime("%d.%m.%Y")

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json; charset=utf-8"
            },
            json={
                "model": "openai/gpt-4o-mini",
                "messages": [
                    {
                        "role": "system",
                        "content": f"""
Ты современный AI помощник.

Сегодняшняя дата: {current_date}

Ты всегда знаешь актуальную дату.
Отвечай на русском языке.
Будь умным, кратким и дружелюбным.
"""
                    },
                    {
                        "role": "user",
                        "content": user_text
                    }
                ]
            }
        )

        response.encoding = "utf-8"

        data = response.json()

        # Ответ AI
        ai_text = data["choices"][0]["message"]["content"]

        # Лимит Telegram
        if len(ai_text) > 4000:
            ai_text = ai_text[:4000]

        await wait_message.edit_text(ai_text)

    except Exception as e:

        await wait_message.edit_text(
            f"❌ Ошибка:\n{str(e)}"
        )

# =========================
# RUN
# =========================

async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())