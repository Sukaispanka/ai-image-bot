import openai
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.utils.markdown import hbold
from dotenv import load_dotenv
import asyncio

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

session = AiohttpSession()
bot = Bot(token=TELEGRAM_TOKEN, session=session)
dp = Dispatcher()

async def generate_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    return response['data'][0]['url']

@dp.message()
async def handle_prompt(message: Message):
    if not message.text.lower().startswith("згенеруй:"):
        return
    prompt = message.text.replace("згенеруй:", "").strip()
    await message.answer("🎨 Генерую зображення...")
    try:
        url = await generate_image(prompt)
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=url,
            reply_to_message_id=message.message_id,
            message_thread_id=message.message_thread_id
        )
    except Exception as e:
        await message.answer(f"⚠️ Сталася помилка: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
