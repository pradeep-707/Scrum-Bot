from mongoengine import StringField, ListField, ReferenceField, DateTimeField, Document
from .helpers import notEmpty
from .members import Member
from datetime import datetime

class Message(Document):
    messageId=StringField(required=True, primary_key=True, validation=notEmpty)
    message=StringField(required=True)
    tags=ListField(StringField(max_length=20))
    author=ReferenceField(Member, required=True)
    replies=ListField(ReferenceField("self"))
    parentMessage=ReferenceField("self")
    timeStamp=DateTimeField(default=datetime.now())
