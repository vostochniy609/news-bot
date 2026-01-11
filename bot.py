import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart

# ================= НАСТРОЙКИ =================

BOT_TOKEN = os.getenv("8405870113:AAF5NkAeWHnIS3IAxcPjoDVa0FxVUSfXGOs")  # токен через Render Variables
ADMIN_ID = int(os.getenv("8155665799"))  # твой Telegram ID (числом)

# =============================================

logging.basicConfig(level=logging.INFO)


async def main():
    if not BOT_TOKEN or not ADMIN_ID:
        raise RuntimeError("Не заданы BOT_TOKEN или ADMIN_ID")

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    @dp.message(CommandStart())
    async def start(message: Message):
        await message.answer(
            "Отправь новость:\n"
            "• текст\n"
            "• фото\n"
            "• видео\n"
            "• документ\n\n"
            "Сообщение будет передано в редакцию."
        )

    @dp.message(
        F.text
        | F.photo
        | F.video
        | F.document
        | F.voice
        | F.audio
        | F.video_note
    )
    async def forward_to_admin(message: Message):
        try:
            await message.forward(chat_id=ADMIN_ID)
        except Exception as e:
            logging.error(f"Ошибка пересылки: {e}")
            await message.answer("Ошибка отправки. Попробуй позже.")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

