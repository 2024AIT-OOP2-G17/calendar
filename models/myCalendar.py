from peewee import Model, CharField, IntegerField
from .db import db

class MyCalendar(Model):
    name = CharField()
    date = IntegerField()

    class Meta:
        database = db