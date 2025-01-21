from peewee import SqliteDatabase
from .db import db
from .eventCalendar import EventCalendar
from .make import Make
from .achieve import Achieve

MODELS = [
    EventCalendar,
    Make,
    Achieve
]

# データベースの初期化関数
def initialize_database():
    db.connect()
    db.create_tables(MODELS, safe=True)
    db.close()