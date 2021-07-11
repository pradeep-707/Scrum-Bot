from mongoengine import StringField, IntField, DateTimeField, Document
from .helpers import notEmpty


class Member(Document):
    name = StringField(required=True, max_length=50, validation=notEmpty)
    rollno = IntField(
        required=True,
        min_value=100000000,
        max_value=200000000,
        unique=True,
        validation=notEmpty,
    )  # should be 9 digit
    password = StringField(required=True, validation=notEmpty)
    batch = IntField(required=True, validation=notEmpty)
    discordHandle = StringField(
        required=True, max_length=50, unique=True, validation=notEmpty
    )
