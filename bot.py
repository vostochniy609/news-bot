import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart

logging.basicConfig(level=logging.INFO)

# ===== НАСТРОЙКИ ЧЕРЕЗ RENDER VARIABLES =====
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
# ===========================================


async def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN не задан")
    if ADMIN_ID == 0:
        raise RuntimeError("ADMIN_ID не задан")

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
            "Сообщение будет передано администратору."
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
        # ❗ НЕ пересылать сообщения админа самому себе
        if message.from_user.id == ADMIN_ID:
            return

        await message.forward(chat_id=ADMIN_ID)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())



