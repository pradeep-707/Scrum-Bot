from pydantic import BaseModel, Field
from typing import Any, List
from datetime import datetime

from models.scrum import Scrum

from schema.dbmodel import DBModelMixin
from schema.messages import messageListHelper

class ScrumInDBSchema(DBModelMixin):
    name: str = Field(...)
    created_at: datetime = Field(...)
    messages: List[Any]


# API Response Models
class StartScrumResponse(BaseModel):
    scrumId: str = Field(...)
    scrumName: str = Field(...)

class EndScrumResponse(BaseModel):
    scrumName: str = Field(...)

def scrumHelper(scrum: Scrum):
    """Converts a single scrum document returned by a mongo to a dict"""

    return {
        "id": scrum.id,
        "objId": str(scrum.id),
        "mongoDocument": scrum,
        "name": scrum.name,
        "created_at": scrum.created_at,
        "messages": messageListHelper(scrum.messages)
    }