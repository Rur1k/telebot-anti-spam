from config import admin_id
from aiogram import types
from aiogram import executor
from load_all import bot, dp


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Ответ на команду старт")


@dp.message_handler(commands=['admin'])
async def process_start_command(message: types.Message):
    await message.reply("Ответ на команду админ")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
