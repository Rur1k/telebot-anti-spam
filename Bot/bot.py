from config import admin_id
from aiogram import types
from aiogram import executor
from load_all import bot, dp, pg_db
from models import User, MessageCount
from peewee import *
import datetime


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Ответ на команду старт")


@dp.message_handler(commands=['admin'])
async def process_admin_command(message: types.Message):
    await message.reply("Ответ на команду админ")


@dp.message_handler()
async def save_user_and_msg(message: types.Message):
    # Проверка на уникальность пользователя который пишет, если пользователь уникальный, записывает его в бд.
    if not User.select().where(User.id_user == message.from_user.id):
        User.create(id_user=message.from_user.id, datetime=datetime.datetime.now(), chat_id=message.chat.id)

    # Проверка на дубль последнего сообщения по пользователю.
    last_id_message = MessageCount.select(fn.Max(MessageCount.id)).where(MessageCount.user_id ==
                                                                         message.from_user.id and
                                                                         MessageCount.chat_id == message.chat.id).scalar()

    last_message = MessageCount.select(MessageCount.message).where(MessageCount.id == last_id_message and
                                                                   MessageCount.chat_id == message.chat.id).scalar()

    print("Чат:"+str(message.chat.id)+"=="+str(last_id_message)+": "+str(last_message))

    if message.text == last_message:
        print('Это дубль, он будет удален')
        await bot.delete_message(message.chat.id, message.message_id)
    else:
        MessageCount.create(user_id=message.from_user.id, datetime=datetime.datetime.now(),
                            message=message.text, chat_id=message.chat.id)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
