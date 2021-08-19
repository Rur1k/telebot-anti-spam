import peeweedbevolve
from load_all import pg_db
from peewee import *


class BaseModel(Model):
    class Meta:
        database = pg_db


class Status(BaseModel):
    id = PrimaryKeyField(unique=True)
    name = CharField(column_name='name', max_length=32)

    class Meta:
        table_name = 'Status'


class Type(BaseModel):
    id = PrimaryKeyField(unique=True)
    name = CharField(column_name='name', max_length=32)

    class Meta:
        table_name = 'Types'


class Keyword(BaseModel):
    id = PrimaryKeyField(unique=True)
    word = CharField(column_name='word', max_length=64)
    type = ForeignKeyField(Type, column_name='type')

    class Meta:
        table_name = 'Keywords'


class User(BaseModel):
    id_user = PrimaryKeyField(column_name='id')
    datetime = DateTimeField(column_name='datetime')
    is_admin = CharField(max_length=16, column_name='is_admin', default=0)
    chat_id = IntegerField(null=True)

    class Meta:
        table_name = 'Users'


class MessageCount(BaseModel):
    user_id = ForeignKeyField(User, column_name='user_id')
    message = TextField(column_name='message')
    datetime = DateTimeField(column_name='datetime')
    chat_id = IntegerField(null=True)

    class Meta:
        table_name = 'Messages_counters'


if __name__ == '__main__':
    pg_db.evolve(interactive=False)

