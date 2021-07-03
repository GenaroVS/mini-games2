from flask_mongoengine import MongoEngine
import mongoengine as me
import datetime

db = MongoEngine()

levels = ('beginner', 'intermediate', 'expert')

class Players(me.Document):
    name = me.StringField(max_length=3, required=True)
    score = me.IntField(required=True)
    date = me.DateTimeField(default=datetime.date.today())
    level = me.StringField(required=True, choices=levels)
    meta = {
        'indexes': ['#level'],
        'index_opts': {
            'sparse': True
        },
        'ordering': ['score']
    }