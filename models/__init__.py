from peewee import SqliteDatabase
from .db import db
from .myCalendar import MyCalendar
MODELS=[
    MyCalendar
]
def initialize_database():
    db.connect()
    db.create_tables(MODELS, safe=True)
    db.close()