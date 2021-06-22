from fastapi import APIRouter, Body, Response
from fastapi.encoders import jsonable_encoder
import logging

from app.helper import ResponseModel, ErrorResponseModel

from controllers.constants import findCurrentScrum, setCurrentScrum
from controllers.scrum import createScrum, findScrumNameWithTheGivenId
from controllers.messages import AddMessageToDataBase, UpdateMessageInDatabase

from schema.response import GenericResponseSchema
from schema.scrum import StartScrumResponse, EndScrumResponse
from schema.messages import CreateMessageSchema, CreateMessageResponseModel,\
                            UpdateMessageSchema, UpdateMessageResponeModel

router = APIRouter()



"""
* Start Scrum
* End Scrum

* POST MESSAGE
* PUT MESSAGE
* DELETE MESSAGE

? TODO 
- adding replies and messages 

"""

@router.get("/scrum/start", response_description="Starts a scrum", response_model=GenericResponseSchema[StartScrumResponse])
def startScrum():
    # Check if a scrum is already active
    # if not start a scrum and update config table
    try:
        scrum = findCurrentScrum()
        assert not scrum
        resp  = createScrum()
        setCurrentScrum(scrumId=resp["data"]["scrumId"])
        return ResponseModel(data=resp["data"], message="A scrum has been started")
    
    except AssertionError as _:
            # a scrum is already going on, sending 400
            return ErrorResponseModel(message="A scrum is already active", 
            error={"err": "A scrum with the id {} is already active".format(scrum)}, statuscode=400)
    
    except Exception as e:
        logging.error("Something went wrong, couldn't create a scrum", e)
        return ErrorResponseModel(message="Couldn't create a scrum, try again later", 
        error={"error": e}, statuscode=500)


@router.get("/scrum/end", response_description="Ends an active scrum", response_model=GenericResponseSchema[EndScrumResponse])
def endScrum():
    try:
        scrum = findCurrentScrum()
        assert scrum
        resp = findScrumNameWithTheGivenId(scrum)

        # unset active scrum in constants collection
        setCurrentScrum()

        return ResponseModel(data=resp["data"], message="Ended {}".format(resp["data"]["scrumName"]))

    except AssertionError as _:
        return ErrorResponseModel(message="No scrum is active", 
            error={"err": "No scrum is active to end"}, statuscode=400)
    except Exception as e:
        logging.error("Something went wrong, couldn't end scrum", e)

        return ErrorResponseModel(message="Couldn't end scrum, try again later", 
        error={"error": e}, statuscode=500)


@router.post("/message", response_description="Adds a message to the active scrum", 
            response_model=GenericResponseSchema[CreateMessageResponseModel]
            )
def addMessage(message: CreateMessageSchema = Body(...)):
    # add message and send True or False
    resp = AddMessageToDataBase(message=message, isParsed=True)
    
    return ( ResponseModel(data={"success": resp["data"]}, message=resp["message"]) \
    if(resp["statusCode"] == 200) \
    else ErrorResponseModel(message=resp["message"], error={"error":resp["error"]}, statuscode=resp["statusCode"]))


@router.put("/message", 
            response_description="Updates the message content and tags for the message with the given messageId",
            response_model=GenericResponseSchema[UpdateMessageResponeModel]
            )
def updateMessage(newMessage: UpdateMessageSchema = Body(...)):
    # Update message and send True or False
    resp = UpdateMessageInDatabase(message=newMessage, isParsed=True)
    
    return ( ResponseModel(data={"success": resp["data"]}, message=resp["message"]) \
    if(resp["statusCode"] == 200) \
    else ErrorResponseModel(message=resp["message"], error={"error":resp["error"]}, statuscode=resp["statusCode"]))
