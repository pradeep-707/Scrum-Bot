from fastapi import APIRouter, Body, Response
from fastapi.encoders import jsonable_encoder

from schema.members import CreateMemberSchema, LoginModel
from controllers.auth import register, login
from app.helper import ResponseModel, ErrorResponseModel

router = APIRouter()


# Register Route
@router.post("/register", response_description="Add member data to database")
async def registerUser(response: Response, member: CreateMemberSchema = Body(...)):
    member.hashPassword()
    data = jsonable_encoder(member)
    resp = register(data)
    response.status_code = resp["statusCode"]
    if resp["statusCode"] == 200:
        return ResponseModel(resp["statusMessage"], resp["message"])
    return ErrorResponseModel(resp["error"], resp["statusCode"], resp["message"])


@router.post("/login", response_description="a JWT bearer token")
async def loginUser(response: Response, creds: LoginModel = Body(...)):
    data = jsonable_encoder(creds)
    resp = login(data["rollno"], data["password"])
    response.status_code = resp["statusCode"]
    if resp["statusCode"] == 200:
        return ResponseModel(resp["data"], resp["message"])
    return ErrorResponseModel(resp["error"], resp["statusCode"], resp["message"])
