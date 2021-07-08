from logging import error
from fastapi import APIRouter, Body, Response
from datetime import datetime
from typing import Optional

from controllers.scrum import (
    findAllScrums,
    findAllScrumsBetweenGivenInterval,
    findScrumWithGivenId,
)
from controllers.messages import (
    getAllDiscussionsByAnAuthor,
    getDiscussionsWithLimitAndOffset,
)
from controllers.members import getAllMembers, getMemberWithGivenId

from schema.response import GenericResponseSchema
from schema.scrum import (
    GetAllScrumsBetweenGivenIntervalResponseModel,
    GetAllScrumsResponseModel,
    GetScrumWithGivenIdResponseModel,
)
from schema.messages import GetDiscussionsPaginatedResponseModel
from schema.members import GetAllMembersResponseModel, GetSingleMemberResponseModel

from app.helper import ResponseModel, ErrorResponseModel
from app.utils import validateDateString

router = APIRouter()


@router.get(
    "/scrums",
    response_description="Gets all scrums",
    response_model=GenericResponseSchema[GetAllScrumsResponseModel],
)
def getAllScrums():
    """Finds all the scrums and returns an array of scrums"""
    resp = findAllScrums(excludeMessages=True, isParsed=True)
    if resp["statusCode"] == 200:
        return ResponseModel(data={"scrums": resp["data"]})
    return ErrorResponseModel(error={"error": resp["error"]}, statuscode=500)


@router.get(
    "/scrums/",
    response_description="Gets all scrums between the given interval. Date should be of the format DD-MM-YYYY",
    response_model=GenericResponseSchema[GetAllScrumsBetweenGivenIntervalResponseModel],
)
def getAllScrumsInGivenInterval(start: str, end: str):
    """Finds all the scrums in the given interval.
    Both the dates(start and end) should be of the format **DD-MM-YYYY**."""
    ((startDate, endDate), errorMsg) = validateDateString(start, end)

    if errorMsg:
        return ErrorResponseModel(error={"error": errorMsg}, statuscode=400)

    resp = findAllScrumsBetweenGivenInterval(
        start=startDate, end=endDate, isParsed=True
    )
    if resp["statusCode"] == 200:
        return ResponseModel(data={"scrums": resp["data"]})
    return ErrorResponseModel(error={"error": resp["error"]}, statuscode=500)


@router.get(
    "/scrums/{scrumId}",
    response_description="The scrum with the given id along with its disussions along with replies",
    response_model=GenericResponseSchema[GetScrumWithGivenIdResponseModel],
)
def getScrumWithGivenId(scrumId: str):
    """Finds the scrums with the given id and returns a the scrum details and
    all the **discussions** which occurred during that scrum."""

    resp = findScrumWithGivenId(scrumId=scrumId, isParsed=True)

    if [resp["statusCode"] == 200]:
        return ResponseModel(data={"scrum": resp["data"]}, message=resp["message"])

    if [resp["statusCode"] == 404]:
        return ErrorResponseModel(
            error=resp["error"], statuscode=404, message=resp["message"]
        )

    return ErrorResponseModel(error={"error": resp["error"]}, statuscode=500)


@router.get(
    "/discussions/",
    response_description="A array of all the queried messages",
    response_model=GenericResponseSchema[GetDiscussionsPaginatedResponseModel],
)
def getDiscussionsPaginated(
    limit: Optional[int] = None, offset: int = 0, author: Optional[str] = None
):
    """Finds all the discussions with the given parameters and returns an array of messages.
    - The parameters can be either
        1. **Limit and offset** - Pagination
        2. **Author** - Gets all the discussions authored by the given user.
    - A request can contain limit and offest **or** author. **It cannot contain both.**"""
    resp = None

    if limit and not author:
        resp = getDiscussionsWithLimitAndOffset(
            limit=limit, offset=offset, isParsed=True
        )
    elif author and not limit:
        resp = getAllDiscussionsByAnAuthor(authorId=author, isParsed=True)

    if not resp:
        return ErrorResponseModel(
            statuscode=400,
            error="The provided parameters are incorrect. \
            The allowed parameters are \n 1. ?limit=Number&offset=Number \n 2. ?author=String",
            message="Bad request",
        )

    if resp["statusCode"] == 200:
        return ResponseModel(
            data={"discussions": resp["data"]}, message=resp["message"]
        )

    if resp["statusCode"] == 404:
        return ErrorResponseModel(
            error=resp["error"], statuscode=404, message=resp["message"]
        )

    return ErrorResponseModel(error={"error": resp["error"]}, statuscode=500)


@router.get(
    "/members",
    response_description="Returns an array of all the members along with their details",
    response_model=GenericResponseSchema[GetAllMembersResponseModel],
)
def getAllMembers():
    """Finds and returns an array of all the members along with their details."""
    resp = getAllMembers(isParsed=True)

    if resp["statusCode"] == 200:
        return ResponseModel(data={"members": resp["data"]}, message=resp["message"])

    return ErrorResponseModel(error={"error": resp["error"]}, statuscode=500)


@router.get(
    "/members/{memberId}",
    response_description="Details of the user with the given userId",
    response_model=GenericResponseSchema[GetSingleMemberResponseModel],
)
def getSingleMember(memberId: str):
    """Finds the member with the given user id"""
    resp = getMemberWithGivenId(id=memberId, isParsed=True)

    if resp["statusCode"] == 200:
        return ResponseModel(data={"member": resp["data"]}, message=resp["message"])

    if [resp["statusCode"] == 404]:
        return ErrorResponseModel(
            error=resp["error"], statuscode=404, message=resp["message"]
        )

    return ErrorResponseModel(error={"error": resp["error"]}, statuscode=500)
