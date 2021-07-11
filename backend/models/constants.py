from mongoengine import StringField, EnumField, DateTimeField, Document
from enum import Enum

from app.config import CONSTANTS


def _createConstDict():
    dict = {}
    for c in CONSTANTS:
        dict[c] = c.lower()
    return dict


ConstantsEnum = Enum("ConstantsEnum", _createConstDict())


class Constant(Document):
    name = EnumField(ConstantsEnum, required=True, unique=True)
    value = StringField(required=True)
