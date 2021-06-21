from datetime import datetime
from typing import Any, Optional
from mongoengine import ObjectIdField
from bson import ObjectId

from pydantic import BaseModel, Field


class DateTimeModelMixin(BaseModel):
    created_at: Optional[datetime] = Field(..., alias="createdAt")
    updated_at: Optional[datetime] = Field(..., alias="updatedAt")


class PyObjectId(ObjectId):
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)


class DBModelMixin(BaseModel):
    id : Optional[PyObjectId]
    objId : Optional[str] = None
    mongoDocument: Optional[Any] # store the actual mongo document in this