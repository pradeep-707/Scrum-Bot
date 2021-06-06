from typing import Optional

from pydantic import BaseModel, EmailStr, Field

class MemberSchema(BaseModel):
    """Member Schema"""
    fullname: str = Field(...)
    rollno: int = Field(..., gt=100000000, lt=200000000) # random, make sure the rollno is 9 digit
    batch: int = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "rollno": 112119006,
                "batch": 2023
            }
        }

class UpdateMemberModel(BaseModel):
    """Update member Member Schema. 
    Can contain one or more field fron {fullname, rollno, batch}"""
    fullname: Optional[str]
    rollno: Optional[int]
    batch: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "rollno": 112119006,
                "batch": 2023
            }
        }

def member_helper(member):
    """converts a single student document returned by mongo to a dict"""
    return {
        "id": str(member["_id"]),
        "fullname": member["fullname"],
        "rollno": member["rollno"],
        "batch": member["batch"],
    }