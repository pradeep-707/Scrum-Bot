from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from ..models.members import MemberSchema
from ..controllers.auth import register
from ..app.helper import ResponseModel, ErrorResponseModel

router = APIRouter()


# Register Route
@router.post("/", response_description="Add member data to database")
async def register(member: MemberSchema = Body(...)):
    data = jsonable_encoder(member)
    member.hashPassword()
    resp = register(data)
    if (resp["statusCode"] == 200):
        return ResponseModel(resp["tatusMessage"], resp["message"])
    return ErrorResponseModel(resp["error"], resp["statusCode"],
                              resp["message"])
