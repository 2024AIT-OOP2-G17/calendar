from peewee import Model, CharField,IntegerField, DateField
from .db import db

class Achieve(Model):
    year = IntegerField()
    month = IntegerField()
    day = IntegerField()
    title = CharField()
    todo = CharField()
    doneDay = CharField()

    class Meta:
        database = db
