from mongoengine import StringField, ListField, ReferenceField, DateTimeField, BooleanField, LazyReferenceField, Document, PULL, CASCADE
from .helpers import notEmpty
from .members import Member
from datetime import datetime

class Message(Document):
    messageId=StringField(required=True, primary_key=True, validation=notEmpty)
    message=StringField(required=True)
    tags=ListField(StringField(max_length=20))
    author=ReferenceField(Member, required=True)
    isDiscussion=BooleanField(required=True)
    replies=ListField(ReferenceField("self",reverse_delete_rule=PULL)) # will delete all replies when a message is deleted
    parentMessage=ReferenceField("self", reverse_delete_rule=CASCADE)
    timeStamp=DateTimeField(default=datetime.now())
