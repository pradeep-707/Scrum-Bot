import logging
from bson import ObjectId
from typing import Union

from app.helper import parseControllerResponse

from models.members import Member
from schema.members import MemberInDBSchema, memberHelper


def getAllMembersFromDB(**kwargs):
    """Finds and returns all the registered members"""

    isResponseParsed = kwargs.get("isParsed", False)
    logging.info("Trying to find the user with the id=", id)

    try:
        rawMembersData = Member.objects()

        parsedMembers = [
            MemberInDBSchema(**memberHelper(rawMember)) for rawMember in rawMembersData
        ]

        logging.info("Found all the users")
        if not isResponseParsed:
            return parsedMembers

        resp = [
            parsedMember.dict(exclude={"mongoDocument"})
            for parsedMember in parsedMembers
        ]
        return parseControllerResponse(
            data=resp, statuscode=200, message="Successfully found the users"
        )

    except Exception as e:
        helpfulErrorMessage = "Couldn't find all the users due to " + e

        logging.error(helpfulErrorMessage)
        if isResponseParsed:
            return parseControllerResponse(
                statuscode=500,
                message="Something went wrong, try again later",
                error=helpfulErrorMessage,
            )
        raise helpfulErrorMessage


def getMemberFromDiscordHandle(discordHandle: str):
    """Finds and returns the user with the given discord handle, if
    such a user doesn't exist, return None"""
    try:
        member_ = Member.objects(discordHandle=discordHandle).first()
        assert member_
        member = MemberInDBSchema(**memberHelper(member_))
        return member
    except AssertionError as _:
        # if the member is not found, raise a ValueError
        return None
    except Exception as e:
        raise Exception(
            "Couldn't find a user with the discord handle \
            {}, due to {}".format(
                discordHandle, e
            )
        )


def getMemberWithGivenId(id: Union[str, ObjectId], **kwargs):
    """Finds and returns the user with the given id, if
    such a user doesn't exist, return None"""

    isResponseParsed = kwargs.get("isParsed", False)

    logging.info("Trying to find the user with the id=", id)
    try:

        user = Member.objects(id=id).first()

        assert user

        logging.debug("Found a user {}, with the id={}".format(memberHelper(user), id))
        logging.info("Found the user with id=", id)

        if not isResponseParsed:
            return MemberInDBSchema(**memberHelper(user))

        return parseControllerResponse(
            data=(MemberInDBSchema(**memberHelper(user))).dict(
                exclude={"mongoDocument"}
            ),
            statuscode=200,
            message="Successfully found the user",
        )

    except AssertionError as _:
        # user was not found, return none or parsed response
        logging.info("A user with id={} does not exist".format(id))

        if isResponseParsed:
            return parseControllerResponse(
                data=None,
                statuscode=404,
                message="User not found",
                error="A user with id={} does not exist".format(id),
            )
        return None

    except Exception as e:
        helpfulErrorMsg = "Couldn't find a user with the userId {}, due to {}".format(
            id, e
        )
        logging.error(helpfulErrorMsg)

        if isResponseParsed:
            return parseControllerResponse(
                data=None,
                statuscode=500,
                message="Something went wrong, try again later.",
                error=helpfulErrorMsg,
            )
        raise helpfulErrorMsg
