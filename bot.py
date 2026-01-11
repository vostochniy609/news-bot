from aiogram import Bot, Dispatcher, executor, types

import os
BOT_TOKEN = os.getenv("8405870113:AAF5NkAeWHnIS3IAxcPjoDVa0FxVUSfXGOs")
ADMIN_ID = 8155665799

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        "Отправьте новость:"
    )


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_text(message: types.Message):
    await bot.send_message(
        ADMIN_ID,
        f"📰 ТЕКСТОВАЯ НОВОСТЬ\n"
        f"От: @{message.from_user.username or message.from_user.id}\n\n"
        f"{message.text}"
    )
    await message.answer("Новость отправлена на модерацию.")


@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def handle_photo(message: types.Message):
    await bot.send_photo(
        ADMIN_ID,
        message.photo[-1].file_id,
        caption=(
            "📰 НОВОСТЬ (ФОТО)\n"
            f"От: @{message.from_user.username or message.from_user.id}\n\n"
            f"{message.caption or 'Без подписи'}"
        )
    )
    await message.answer("Новость отправлена.")


@dp.message_handler(content_types=types.ContentTypes.VIDEO)
async def handle_video(message: types.Message):
    await bot.send_video(
        ADMIN_ID,
        message.video.file_id,
        caption=(
            "📰 НОВОСТЬ (ВИДЕО)\n"
            f"От: @{message.from_user.username or message.from_user.id}\n\n"
            f"{message.caption or 'Без подписи'}"
        )
    )
    await message.answer("Новость отправлена.")


if __name__ == "__main__":
    executor.start_polling(dp)
