import asyncio
import logging
import os

from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.getenv("RENDER_EXTERNAL_URL") + WEBHOOK_PATH


async def start_bot():
    if not BOT_TOKEN or not ADMIN_ID:
        raise RuntimeError("BOT_TOKEN или ADMIN_ID не заданы")

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
    async def forward(message: Message):
        await message.forward(ADMIN_ID)

    await bot.set_webhook(WEBHOOK_URL)

    app = web.Application()

    async def handle(request):
        update = await request.json()
        await dp.feed_webhook_update(bot, update)
        return web.Response()

    app.router.add_post(WEBHOOK_PATH, handle)

    runner = web.AppRunner(app)
    await runner.setup()

    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, host="0.0.0.0", port=port)
    await site.start()

    logging.info("Webhook запущен")


async def main():
    await start_bot()
    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())


