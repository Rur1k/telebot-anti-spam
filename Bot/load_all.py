import asyncio
import logging

from playhouse.postgres_ext import PostgresqlExtDatabase
from config import host, PG_PASS, PG_USER, TOKEN
from aiogram import Bot, Dispatcher

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO)

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Подключние к БД
pg_db = PostgresqlExtDatabase('db_bot', user=PG_USER, password=PG_PASS, host=host)


