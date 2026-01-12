import os
import asyncio
import logging

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.exceptions import TelegramRetryAfter
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # https://your-service.onrender.com/webhook
PORT = int(os.getenv("PORT", 10000))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()


# ===== ХЕНДЛЕР =====
@dp.message()
async def echo(message: Message):
    await message.answer(message.text)


# ===== WEBHOOK =====
async def on_startup(app: web.Application):
    try:
        await bot.set_webhook(WEBHOOK_URL)
        logging.info("Webhook установлен")
    except TelegramRetryAfter as e:
        logging.warning(f"FloodWait при setWebhook: {e.retry_after}s")


async def on_shutdown(app: web.Application):
    await bot.session.close()


def main():
    app = web.Application()

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    ).register(app, path="/webhook")

    setup_application(app, dp, bot=bot)

    web.run_app(app, host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    main()



