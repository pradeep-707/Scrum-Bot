from logging import error
from fastapi import APIRouter, Body, Response

from controllers.scrum import findAllScrums

from app.helper import ResponseModel, ErrorResponseModel

router = APIRouter()

@router.get("/scrums", response_description="Gets all scrums")
def getAllScrums():
    resp = findAllScrums(excludeMessages=True, isParsed=True)
    if resp["statusCode"] == 200:
        return ResponseModel(data={"scrums": resp["data"]})
    return ErrorResponseModel(error={"error":resp["error"]}, statuscode=500)
