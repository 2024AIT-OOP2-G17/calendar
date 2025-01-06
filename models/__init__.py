from peewee import SqliteDatabase
from .db import db
from .eventCalendar import EventCalendar

# データベースの初期化関数
def initialize_database():
    db.connect()
    db.create_tables([EventCalendar], safe=True)
    db.close()