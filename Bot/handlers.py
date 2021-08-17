from aiogram import types
from load_all import bot, dp, pg_db


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Ответ на команду старт")
