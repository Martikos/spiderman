from settings import *
import mongoengine
from mongoengine import *

def connect():
    mongoengine.connect(
            MONGO_DATABASE_NAME,
            host=MONGO_HOST,
            port=MONGO_PORT,
            username=MONGO_USERNAME,
            password=MONGO_PASSWORD)

connect()


class Video(object):

    campaign_id = ObjectIdField()
    youtube_id = StringField()
    used = BooleanField()
