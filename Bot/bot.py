from config import admin_id
from aiogram import types
from aiogram import executor
from load_all import bot, dp, pg_db
from models import User, MessageCount, Function, Keyword
from peewee import *
import datetime


# Проверка пользователя на уникальность, если такого нет, то делает новую запись с пользователем
def save_new_user(user_id, chat_id, user_name):
    if not User.select().where(User.id_user == user_id):
        User.create(id_user=user_id, datetime=datetime.datetime.now(), chat_id=chat_id, user_name=user_name)


# Сохраняет в бд сообщение абонента
def save_message(user_id, chat_id, message_id, message):
    MessageCount.create(user_id=user_id, datetime=datetime.datetime.now(), message=message, chat_id=chat_id,
                        message_id=message_id)


# Назначение прав администратора
def appointment_admin(user_id):
    new_admin = User.update(is_admin=1).where(User.id_user == user_id)
    new_admin.execute()


# Проверка на админа
def is_admin(user_id):
    status = User.select(User.is_admin).where(User.id_user == user_id).scalar()
    if int(status) == 1:
        return True
    else:
        return False


# Создает базовую функции управления
def create_base_functions():
    if not Function.select().where(Function.id == 1):
        Function.create(id=1, name='Delete new key word')
    if not Function.select().where(Function.id == 2):
        Function.create(id=2, name='Delete new msg in repeat')
    if not Function.select().where(Function.id == 3):
        Function.create(id=3, name='Delete old key word')
    pass


# Запрос на проверку влючения базовых функций.
def is_enable(function_id):
    enable = Function.select(Function.is_enable).where(Function.id == function_id).scalar()
    if int(enable) == 1:
        return True
    else:
        return False


# Проверяет вводимое сообщение на наличие запрещенных слов
def is_forbidden_word(text):
    forbidden_words = Keyword.select()
    for word in forbidden_words:
        if word.word in text.lower():
            return True
    return False


# Являеться ли введенное сообщение дублем веденного ранее
def is_repeat_last_message(user_id, chat_id, message):
    message_id = MessageCount.select(fn.max(MessageCount.id)).where((MessageCount.user_id == user_id) &
                                                                    (MessageCount.chat_id == chat_id)).scalar()
    if message_id:
        last_message = MessageCount.select(MessageCount.message).where(MessageCount.id == message_id).scalar()
        if message.lower() == last_message.lower():
            return True
    return False


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    save_new_user(message.from_user.id, message.chat.id, message.from_user.username)
    create_base_functions()

    await message.reply("Ответ на команду старт")


@dp.message_handler(commands=['admin'])
async def process_admin_command(message: types.Message):
    save_new_user(message.from_user.id, message.chat.id, message.from_user.username)
    await bot.delete_message(message.chat.id, message.message_id)
    if is_admin(message.from_user.id):
        await bot.send_message(message.from_user.id, 'Жду команд')
    else:
        await bot.send_message(message.from_user.id, 'Вы не администратор, комана "admin" не доступна')


@dp.message_handler(commands=['giveadmin'])
async def process_give_admin_command(message: types.Message):
    save_new_user(message.from_user.id, message.chat.id, message.from_user.username)
    appointment_admin(message.from_user.id)

    await bot.delete_message(message.chat.id, message.message_id)
    await bot.send_message(message.from_user.id, "Вы назначены администратором, доступна функиция /admin")


@dp.message_handler(commands=['dropoldword'])
async def delete_old_message(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    if is_admin(message.from_user.id):
        message_list = MessageCount.select()
        for one_message in message_list:
            if is_forbidden_word(one_message.message):
                MessageCount[one_message.id].delete_instance()
                await bot.delete_message(one_message.chat_id, one_message.message_id)
    else:
        await bot.send_message(message.from_user.id, 'Вы не администратор, комана "/dropoldword" не доступна')


@dp.message_handler(commands=['userlist'])
async def select_users(message: types.Message):
    user_list = User.select().where(User.chat_id == message.chat.id)
    users = []
    for user in user_list:
        users.append(user.user_name)
    await bot.send_message(message.from_user.id, users)




@dp.message_handler()
async def save_user_and_msg(message: types.Message):
    save_new_user(message.from_user.id, message.chat.id, message.from_user.username)

    if is_enable(1):
        if is_forbidden_word(message.text):
            await bot.delete_message(message.chat.id, message.message_id)
        elif is_enable(2):
            if is_repeat_last_message(message.from_user.id, message.chat.id, message.text):
                await bot.delete_message(message.chat.id, message.message_id)
            else:
                save_message(message.from_user.id, message.chat.id, message.message_id, message.text)
    elif is_enable(2):
        if is_repeat_last_message(message.from_user.id, message.chat.id, message.text):
            await bot.delete_message(message.chat.id, message.message_id)
        else:
            save_message(message.from_user.id, message.chat.id, message.message_id, message.text)
    else:
        save_message(message.from_user.id, message.chat.id, message.message_id, message.text)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
