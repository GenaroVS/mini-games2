from flask_mongoengine import MongoEngine
import mongoengine as me
import datetime

db = MongoEngine()

class Player(me.Document):
    name = me.StringField(max_length=3)
    score = me.IntField()
    date = me.DateTimeField(default=datetime.datetime.now)
    level = me.StringField()
