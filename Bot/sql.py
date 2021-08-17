import logging

from peewee import *

from config import host, PG_PASS, PG_USER

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO)

pg_db = PostgresqlDatabase('db_bot', user=PG_USER, password=PG_PASS, host=host, port=5432)

