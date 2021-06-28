from mongoengine import StringField, ListField, ReferenceField, DateTimeField, Document, PULL
from datetime import datetime
from .messages import Message as MessageModel

class Scrum(Document):
    name= StringField(required=True)
    created_at=DateTimeField(default=datetime.now())
    messages=ListField(ReferenceField(MessageModel, reverse_delete_rule=PULL))

    @classmethod
    def generateName(self):
        """Generates a name for the scrum"""
        dateStr = datetime.now().date().strftime("%A, %d %B %Y") # 'Saturday, 19 June 2021'
        return "Scrum - {}".format(dateStr)
    