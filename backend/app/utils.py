import enum
from datetime import datetime
import logging

from fastapi import Header, Depends, Request, HTTPException
from fastapi.exceptions import HTTPException
import jwt
from pydantic import ValidationError

from .config import (
    JWT_SECRET,
    JWT_ALGORITHM,
    JWT_EXPIRE_TIME,
    JWT_TOKEN_PREFIX,
    AUTH_HEADER_KEY,
    BOT_HEADER_KEY,
    BOT_TOKEN_PREFIX,
)

from schema.jwt import JWTToken, _JWTUser

# generate a jwt with the given data
def generateJwt(data: _JWTUser):
    try:
        algorithm = JWT_ALGORITHM
        jwtSecret = JWT_SECRET
        tokenExpireTime = JWT_EXPIRE_TIME

        payload = JWTToken(**{"sub": data.copy()})

        if tokenExpireTime != 0:
            payload.exp = datetime.now() + tokenExpireTime

        return jwt.encode(payload.dict(), jwtSecret, algorithm=algorithm)
    except Exception as e:
        print("Couldnt generate jwt", e)
        raise Exception(e)


# A class to handle all JWT and Bot authorization
class Authorization(object):
    """Class which handles all authentication related logic"""

    class Config:
        schema = {
            "type": "type of authorization",
            "headerName": "Name of the required header",
            "headerPrefix": "Prefix of the required header",
            "headerData": "content header - prefix",
            "payload": "Contents of the decoded header data",  # only for jwt
        }

    allowedAuthorizationTypes = ["jwt", "bot"]

    def __init__(self, **kwargs):
        allowedKeys = ["type"]
        typeInitHandlers = [self._handle_JwtAuthInit, self._handle_BotAuthInit]

        self.__dict__.update(
            ("type", str(v).lower()) for k, v in kwargs.items() if k in allowedKeys
        )

        if self.type not in self.allowedAuthorizationTypes:
            return self._handle_InvalidAuthorizationTypes(self.name)

        for index, value in enumerate(self.allowedAuthorizationTypes):
            if self.type == value:
                typeInitHandlers[index]()

    def authenticateUser(self, request: Request):
        """Find the correct header from the request obj,
        verifies if the header is in the correct format,
        stores the header playload in headerData"""

        # this is the only function which needs to be called while authenticating users
        # this stores all the necessary data and authenticates user

        headerItems = request.headers.items()

        isHeaderFound = False
        for (headerKey, headerValue) in headerItems:
            if headerKey == self.headerName:
                self._splitHeader(headerValue)
                isHeaderFound = True

        if not isHeaderFound:
            # no auth token, throw a 403
            return self._handle_Raise403Exception(1, (self.headerName,))

        self.verifyHeaderDataAndStorePayload()

    def verifyHeaderDataAndStorePayload(self):
        """Verifies the header data, stores payload (if any)"""
        headerVerifiers = [self._decodeJwt, self._verifyBotHeader]
        for index, value in enumerate(self.allowedAuthorizationTypes):
            if self.type == value:
                headerVerifiers[index]()

    # ? helper methods
    def _handle_JwtAuthInit(self):
        self.headerName = AUTH_HEADER_KEY
        self.headerPrefix = JWT_TOKEN_PREFIX

    def _handle_BotAuthInit(self):
        self.headerName = BOT_HEADER_KEY
        self.headerPrefix = BOT_TOKEN_PREFIX

    def _handle_InvalidAuthorizationTypes(self, code):
        raise Exception(
            "Invalid type received for authorization class declaration, got {}".format(
                code
            )
        )

    def _splitHeader(self, header):
        """Splits the header; stores header payload in headerData
        throws 403 error if the  header is invalid"""

        split = header.split()

        if len(split) != 2 or split[0] != self.headerPrefix:
            # header is invalid, raise a 403 error
            return self._handle_Raise403Exception(2, (header,))

        self.headerData = split[1]
        return

    def _decodeJwt(self):
        """Decodes jwt, and stores playload in the obj"""
        try:
            decodedToken = JWTToken(
                **jwt.decode(self.headerData, JWT_SECRET, JWT_ALGORITHM)
            )
            payload = decodedToken.sub

            if payload == None:
                return self._handle_Raise403Exception(3, tuple())

            # Add playload data to the obj
            self.payload = payload
            return True

        except jwt.PyJWTError as decodeError:
            # unable to decode the token,
            # prolly becoz the user is sending random data
            logging.error("Unable to decode jwt, ", decodeError)
            return self._handle_Raise403Exception(3, tuple())
        except ValidationError as validationError:

            logging.error("jwt token validation failed", validationError)
            return self._handle_Raise403Exception(3, tuple())
        except Exception as e:
            logging.error("Decoding jwt failed, ", e)
            # TODO: Return 500 error

    def _verifyBotHeader(self):
        """Verifies if the bot secret is corret, else throws a 403"""
        # TODO: Finish this
        return True

    def _handle_Raise403Exception(self, errorCode: int, values: tuple):
        """Raises a 403 exception for differnet authentication errors"""

        class ErrorTypes(enum.Enum):
            HeaderNotProvided = 1
            InvalidHeaderFormat = 2
            JWTValidationError = 3
            BotSecretValidationError = 4

        errorDetails = {
            "HeaderNotProvided": "{} header is not provided",
            "InvalidHeaderFormat": "The header entered in in the wrong format {}",
            "JWTValidationError": "Could not validate user. Try again later",
            "BotSecretValidationError": "Bot validartion failed",
        }

        def parseErrorMessage():
            try:
                return errorDetails[ErrorTypes(errorCode).name].format(*values)
            except Exception as e:
                # this is a mistake on our side, so raise a 500 error
                # with a generic messsage for this
                logging.error("Couldn't generate 403 error message ", e)

                raise Exception(
                    "Invalid data provided for string formatting for 403 error, \
                    for the string {}. But got".format(
                        errorDetails[ErrorTypes(errorCode).name]
                    ),
                    values,
                )

        raise HTTPException(status_code=403, detail=parseErrorMessage())


def validateDateString(start: str, end: str):
    """Validates the datesting given for querying scrums"""

    startDateStr = start.split("-")
    endDateStr = end.split("-")

    invalidDateStingErrorMessage = "The given dates {} and {} are of invalid format. \
        It should be of the format DD-MM-YYYY.".format(
        start, end
    )

    try:
        assert len(startDateStr) == 3 and len(endDateStr) == 3, "invalidDateString"

        assert int(endDateStr[2]) > 2000 and int(startDateStr[2]) > 2000, "invalidYear"

        startDate = datetime(
            int(startDateStr[2]), int(startDateStr[1]), int(startDateStr[0])
        )
        endDate = datetime(
            int(endDateStr[2]), int(endDateStr[1]), int(endDateStr[0]) + 1
        )

        assert endDate > startDate, "invalidValues"

        return (startDate, endDate), None

    except AssertionError as e:
        if str(e) == "invalidDateString":
            return (0, 0), invalidDateStingErrorMessage
        if str(e) == "invalidYear":
            return (0, 0), "The year you have entered is invalid"
        if str(e) == "invalidValues":
            return (0, 0), "The start date should be greater than end date"

    except ValueError as _:
        # we get this error when the invalid date is provided for datetime
        # so, return invalid dateStringErrorMessage
        return (0, 0), invalidDateStingErrorMessage
