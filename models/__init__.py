from peewee import SqliteDatabase
from .db import db
from .eventCalendar import EventCalendar
from .make import Make

MODELS = [
    EventCalendar,
    Make
]

# データベースの初期化関数
def initialize_database():
    db.connect()
    db.create_tables(MODELS, safe=True)
    db.create_tables([EventCalendar])
    db.close()