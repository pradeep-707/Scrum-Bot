from logging import error
from fastapi import APIRouter, Body, Response
from datetime import datetime
from typing import Optional
from controllers.members import getAllMembers, getMemberWithGivenId

from controllers.scrum import findAllScrums, findAllScrumsBetweenGivenInterval, findScrumWithGivenId
from controllers.messages import getAllDiscussionsByAnAuthor, getDiscussionsWithLimitAndOffset

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

@router.get("/discussions/")
def getDiscussionsPaginated(limit: Optional[int] = None, offset: int = 0, author: Optional[str] = None):
    # do something
    
    resp = None

    if limit and not author:
        resp = getDiscussionsWithLimitAndOffset(limit=limit, offset=offset, isParsed=True)
    elif author and not limit:
        resp = getAllDiscussionsByAnAuthor(authorId=author, isParsed=True)
    
    if not resp:
        return ErrorResponseModel(statuscode=400, error="The provided parameters are incorrect. \
            The allowed parameters are \n 1. ?limit=Number&offset=Number \n 2. ?author=String",
            message="Bad request")

    if resp["statusCode"] == 200:
            return ResponseModel(data=resp["data"], message=resp["message"])
    
    if resp["statusCode"] == 404:
        return ErrorResponseModel(error=resp["error"], statuscode=404, message=resp["message"])

    return ErrorResponseModel(error={"error":resp["error"]}, statuscode=500)

@router.get("/members", response_description="Returns an array of all the members along with their details")
def getAllMembers():
    resp = getAllMembers(isParsed=True)

    if resp["statusCode"] == 200:
        return ResponseModel(data={"members": resp["data"]}, message=resp["message"])
    
    return ErrorResponseModel(error={"error":resp["error"]}, statuscode=500)

@router.get("/members/{memberId}", response_description="Finds the user with the given userId")
def findSingleMember(memberId: str):
    resp = getMemberWithGivenId(id=memberId, isParsed=True)

    if resp["statusCode"] == 200:
        return ResponseModel(data={"member": resp["data"]}, message=resp["message"])
    
    if[resp["statusCode"] == 404]:
        return ErrorResponseModel(error=resp["error"], statuscode=404, message=resp["message"])


    return ErrorResponseModel(error={"error":resp["error"]}, statuscode=500)
