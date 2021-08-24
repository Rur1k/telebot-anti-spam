import peeweedbevolve
from load_all import pg_db
from peewee import *


class BaseModel(Model):
    class Meta:
        database = pg_db


class State(BaseModel):
    state = IntegerField(null=True, default=0)
    name = CharField(max_length=64)


class BotState(BaseModel):
    chat = IntegerField(null=True)
    state = IntegerField(null=True)


class Keyword(BaseModel):
    id = PrimaryKeyField(unique=True)
    word = CharField(column_name='word', max_length=64)

    class Meta:
        table_name = 'Keywords'


class Function(BaseModel):
    id = PrimaryKeyField(unique=True)
    name = CharField(max_length=32)
    is_enable = CharField(max_length=16, default=0)


class User(BaseModel):
    id = PrimaryKeyField(unique=True)
    id_user = IntegerField(null=True)
    user_name = CharField(max_length=64, null=True)
    datetime = DateTimeField(column_name='datetime')
    is_admin = CharField(max_length=16, column_name='is_admin', default=0)
    chat_id = IntegerField(null=True)

    class Meta:
        table_name = 'Users'


class MessageCount(BaseModel):
    user_id = IntegerField(null=True)
    message_id = IntegerField()
    message = TextField(column_name='message')
    datetime = DateTimeField(column_name='datetime')
    chat_id = IntegerField(null=True)

    class Meta:
        table_name = 'Messages_counters'


if __name__ == '__main__':
    pg_db.evolve(interactive=False)

