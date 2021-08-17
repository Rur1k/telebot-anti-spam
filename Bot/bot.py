from config import admin_id
from aiogram import executor
from load_all import bot, dp


async def on_shutdown(dp):
    await bot.close()


async def on_startup(dp):
    await bot.send_message(admin_id, "Я запущен!")

if __name__ == "__main__":
    executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=on_startup)
