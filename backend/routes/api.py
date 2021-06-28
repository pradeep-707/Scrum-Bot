from logging import error
from fastapi import APIRouter, Body, Response
from datetime import datetime

from controllers.scrum import findAllScrums, findAllScrumsBetweenGivenInterval, findScrumWithGivenId

from app.helper import ResponseModel, ErrorResponseModel
from app.utils import validateDateString

router = APIRouter()

@router.get("/scrums", response_description="Gets all scrums")
def getAllScrums():
    resp = findAllScrums(excludeMessages=True, isParsed=True)
    if resp["statusCode"] == 200:
        return ResponseModel(data={"scrums": resp["data"]})
    return ErrorResponseModel(error={"error":resp["error"]}, statuscode=500)

@router.get("/scrums/", response_description="Gets all scrums between the given interval. Date should be of the format DD-MM-YYYY")
def getAllScrumsInGivenInterval(start: str, end: str):
    ((startDate, endDate), errorMsg) = validateDateString(start, end)

    if errorMsg:
        return ErrorResponseModel(error={"error":errorMsg}, statuscode=400)
    
    resp = findAllScrumsBetweenGivenInterval(start=startDate, end=endDate, isParsed=True)
    if resp["statusCode"] == 200:
        return ResponseModel(data={"scrums": resp["data"]})
    return ErrorResponseModel(error={"error":resp["error"]}, statuscode=500)

@router.get("/scrums/{scrumId}")
def getScrumWithGivenId(scrumId: str):
    resp = findScrumWithGivenId(scrumId=scrumId, isParsed=True)

    if[resp["statusCode"] == 200]:
        return ResponseModel(data=resp["data"], message=resp["message"])
    
    if[resp["statusCode"] == 404]:
        return ErrorResponseModel(error=resp["error"], statuscode=404, message=resp["message"])

    return ErrorResponseModel(error={"error":resp["error"]}, statuscode=500)
