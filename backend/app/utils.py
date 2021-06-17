import enum
from datetime import datetime
import logging

from fastapi import Header, Depends, Request, HTTPException
from fastapi.exceptions import HTTPException
import jwt
from pydantic import ValidationError

from .config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRE_TIME,\
                    JWT_TOKEN_PREFIX, AUTH_HEADER_KEY,\
                    BOT_HEADER_KEY, BOT_TOKEN_PREFIX

from ..schema.jwt import JWTToken

# generate a jwt with the given data
def generateJwt(data: JWTToken.sub):
    try:
        algorithm = JWT_ALGORITHM
        jwtSecret = JWT_SECRET
        tokenExpireTime = JWT_EXPIRE_TIME
        
        payload = JWTToken(**{"sub": data.copy()})

        if tokenExpireTime != 0:
            payload.exp = datetime.now() + tokenExpireTime

        return jwt.encode(payload, jwtSecret, algorithm=algorithm)
    except Exception as e:
        print("Couldnt generate jwt", e)
        raise Exception(e)


# A class to handle all JWT and Bot authorization
class Authorization(object):
    
    allowedAuthorizationTypes=["jwt", "bot"]


    def __init__(self, **kwargs):
        allowedKeys = ["type"]
        typeInitHandlers=[self._handle_JwtAuthInit,self._handle_BotAuthInit]

        self.__dict__.update(("type", str(v).lower()) for k, v in kwargs.items() if k in allowedKeys)
        
        if self.type not in self.allowedAuthorizationTypes:
            return self._handle_InvalidAuthorizationTypes(self.name)
        
        for index, value in enumerate(self.allowedAuthorizationTypes):
            if self.type == value:
                typeInitHandlers[index]()
    
    def getToken(self, request: Request):
        """Find the correct header from the request obj,
        verifies if the header is in the correct format,
        stores the header playload in headerData"""

        headerItems = request.headers.items()

        isHeaderFound = False
        for (headerKey, headerValue) in headerItems:
            if(headerKey == self.headerName):
                self.splitHeader(headerValue)
                isHeaderFound = True
        
        if not isHeaderFound:
            # no auth token, throw a 403
            return self._handle_Raise403Exception(1, (self.headerName,))

    def _decodeJwt(self):
        """Decodes jwt, and stores playload in the obj"""
        try:
            decodedToken = JWTToken(**jwt.decode(self.headerData, JWT_SECRET, JWT_ALGORITHM))
            payload = decodedToken.sub
            
            if payload == None:
                return self._handle_Raise403Exception(3, tuple())

            # Add playload data to the obj
            self.payload = payload
            return

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
            return
        

    def splitHeader(self, header):
        """Splits the header; stores header payload in headerData
        throws 403 error if the  header is invalid"""

        split = header.split();

        if len(split) != 2 or split[0] != self.headerPrefix:
            # header is invalid, raise a 403 error
            return self._handle_Raise403Exception(2, (header,))

        self.headerData = split[1]
        return
        

    # helper methods
    def _handle_JwtAuthInit(self):
        self.headerName = AUTH_HEADER_KEY
        self.headerPrefix = JWT_TOKEN_PREFIX
    
    def _handle_BotAuthInit(self):
        self.headerName = BOT_HEADER_KEY
        self.headerPrefix = BOT_TOKEN_PREFIX

    
    def _handle_InvalidAuthorizationTypes(self, code):
        raise Exception("Invalid type received for authorization class declaration, got {}".format(code))
    

    def _handle_Raise403Exception(self, errorCode : int, values:tuple):
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
            "BotSecretValidationError": "Bot validartion failed"
        }


        def parseErrorMessage():
            try:
                return errorDetails[ErrorTypes(errorCode).name].format(*values)
            except Exception as e:
                # this is a mistake on our side, so raise a 500 error 
                # with a generic messsage for this
                logging.error("Couldn't generate 403 error message ", e)

                raise Exception("Invalid data provided for string formatting for 403 error, \
                    for the string {}. But got".format(errorDetails[ErrorTypes(errorCode).name]), 
                    values)

        raise HTTPException(status_code=403, detail=parseErrorMessage())