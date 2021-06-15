from typing import Optional
from pydantic import BaseModel, Field, validator
import hashlib
import os

class CreateMemberSchema(BaseModel):
    """Member Schema"""
    name: str = Field(...)
    rollno: int = Field(
        ..., gt=100000000,
        lt=200000000)  # random, make sure the rollno is 9 digit
    password: str = Field(...)
    batch: int = Field(...)
    discordHandle: str = Field(...)
    password_repeat: str = Field(...)

    # Check if the discordHandle contains a '#'
    @validator("discordHandle")
    def discordHandleMustContainHash(cls, v):
        if '#' not in v:
            raise ValueError("Discord handle must contain '#'")
        return v

    # Check if password is at least 6 characters long
    @validator("password")
    def passwordLongEnough(cls, v):
        if (len(v) < 6):
            raise ValueError("Password is too short")
        return v

    # check if password and repeat_password match
    @validator("password_repeat")
    def checkPasswordMatch(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError("passwords do not match")
        return v

    # helper function to generate salt and hash for the password
    @classmethod
    def hashPassword(self):
        # genrates 32 random bytes
        salt = os.urandom(32)
        salt = salt.hex()
        # key is generated using https://docs.python.org/3/library/hashlib.html#hashlib.pbkdf2_hmac
        # reccomended to use at least 10^6 iterations of sha_256
        # generates 128 bit key
        key = hashlib.pbkdf2_hmac('sha256', self.password.encode('utf-8'), salt.encode("utf-8"), int(1e6), dklen=128)
        self.password = salt + '.' + key.hex()
        return

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "rollno": 112119006,
                "batch": 2023,
                "discordHandle": "john#1234",
                "password": "password123",
                "password_repeat": "password123"
            }
        }


class UpdateMemberSchema(BaseModel):
    """Update member Member Schema. 
    Can contain one or more field from {name, rollno, batch, discordHandle, password, password_repeat}"""
    name: Optional[str]
    rollno: Optional[int]
    batch: Optional[int]
    discordHandle: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "rollno": 112119006,
                "batch": 2023,
                "discordHandle": "john#1234",
                "password": "password123",
                "password_repeat": "password123"
            }
        }


class LoginModel(BaseModel):
    """Login Model Schema"""

    rollno: int = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "rollno": 112119006,
                "password": "password123"
            }
        }


# HELPER FUNCTIONS

def memberHelper(member):
    """converts a single student document returned by mongo to a dict"""
    return {
        "id": str(member["_id"]),
        "name": member["name"],
        "rollno": member["rollno"],
        "batch": member["batch"],
        "discoardHandle": member["discordHandle"]
    }


def verifyPassword(password: str, inputPassword: str):
    """check if the password and the inputPassword matches

    Args:
        password (str): hashed password stored in the database
        inputPassword (str): plain text password entered by the user which logging in the

    Returns:
        Bool: True if the password matches, False otherwise False
    """
    try:
        [salt, key] = password.split('.')
        # salt = bytes(salt, "utf-8")
        inputKey = hashlib.pbkdf2_hmac('sha256',inputPassword.encode('utf-8'),salt.encode("utf-8"),int(1e6),dklen=128)

        if (inputKey.hex() == key):
            return True
        return False
    except Exception as e:
        # there shdnt be any exception
        print("err : ", e)
