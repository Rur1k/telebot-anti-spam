import peeweedbevolve
from load_all import pg_db
from peewee import *


class BaseModel(Model):
    class Meta:
        database = pg_db


class User(BaseModel):
    id = IntegerField(column_name='id')
    first_name = CharField(column_name='first_name', max_length=64, null=True)
    last_name = CharField(column_name='last_name', max_length=64, null=True)

    class Meta:
        table_name = 'Users'


if __name__ == '__main__':
    pg_db.evolve(interactive=False)

