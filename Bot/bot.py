from config import admin_id
from aiogram import types
from aiogram import executor
from load_all import bot, dp, pg_db
from models import User, MessageCount
import datetime


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Ответ на команду старт")


@dp.message_handler(commands=['admin'])
async def process_admin_command(message: types.Message):
    await message.reply("Ответ на команду админ")


@dp.message_handler()
async def save_user_and_msg(message: types.Message):
    if not User.get(User.id_user == message.from_user.id):
        User.create(id_user=message.from_user.id, datetime=datetime.datetime.now())


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
