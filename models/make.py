from .db import db
from peewee import Model, CharField

class Make(Model):
    title = CharField()

    class Meta:
        database = db