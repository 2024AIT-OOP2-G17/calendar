from peewee import Model, CharField,IntegerField
from .db import db

class EventCalendar(Model):
    add_month = IntegerField()
    add_day = IntegerField()
    add_title = CharField()
    add_todo = CharField()
    add_year = IntegerField()

    class Meta:
        database = db
        
