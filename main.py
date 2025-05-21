import openai
import os
from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)
openai.api_key = OPENAI_API_KEY

async def generate_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    return response['data'][0]['url']

@dp.message_handler()
async def handle_prompt(message: types.Message):
    if not message.text.lower().startswith("згенеруй:"):
        return
    prompt = message.text.replace("згенеруй:", "").strip()
    await message.reply("🎨 Генерую зображення...")
    try:
        url = await generate_image(prompt)
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=url,
            reply_to_message_id=message.message_id,
            message_thread_id=message.message_thread_id
        )
    except Exception as e:
        await message.reply(f"⚠️ Сталася помилка: {e}")

if __name__ == '__main__':
    executor.start_polling(dp)
