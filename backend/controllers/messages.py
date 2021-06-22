from datetime import datetime
import logging
from typing import Union
from enum import Enum, auto

from schema.messages import CreateMessageSchema, UpdateMessageSchema
from schema.members import MemberInDBSchema

from models.messages import Message

from controllers.members import getMemberFromDiscordHandle
from controllers.constants import findCurrentScrum
from controllers.scrum import addMessageToScrum

from app.helper import parseControllerResponse

def AddMessageToDataBase(message: CreateMessageSchema, **kwargs):
    """Adds a message to the database"""
    isResponseParsed = kwargs.get("isParsed", False)

    # Find the user, and do necessary
    try:
        author = getMemberFromDiscordHandle(message.author)
        assert author, "Invalid user"
        currentScrum = findCurrentScrum()

        # scrum needs to be active only when creating a new discussion
        if not message.isReply:
            assert currentScrum, "No scrum is active"

        resp = ( _createReplyForScrum(message=message, author=author) ) \
            if message.isReply \
            else( _createNewDiscussionForScrum(message=message, author=author) )

        logging.info("Got the response of {}, while creating a new message".format(resp.value))

        if resp == MessageControllerHelper.Success:
            if isResponseParsed:
                return parseControllerResponse(data=True, statuscode=200, message="Message added successfully")
            return True
        

        # Commenting it out as this is handled by assert statement
        #
        # if resp == MessageControllerHelper.UserNotFound:
        #     # author was not found
        #     logging.debug("Cannot add message for the user because, \
        #         a user with the given discord handle {} doesn't exist".format(message.author))
        #     if isResponseParsed:
        #         return parseControllerResponse(data=False, statuscode=400, 
        #         message="A user with the given discord handle {} doesn't exist".format(message.author), 
        #         error="A user with the given discord handle {} doesn't exist".format(message.author), 
        #         )
        #     return False
        
        if resp == MessageControllerHelper.ParentMessageNotFound:
            # parent message for reply isn't found,
            # something went wrong in the bot side
            # log reqd data, and return 400
            logging.debug("Couldn't add the message obj {}, \
                as the parent message was not found".format(message.dict()))
            if isResponseParsed:
                return parseControllerResponse(data=False, statuscode=400, 
                message="Parent message not found", 
                error="Couldn't add the message as the parent message was not found", 
                )
            return False

        if resp == MessageControllerHelper.MessageIdTaken:
            logging.debug("Couldn't add the message obj {}, \
                as the message id was taken".format(message.dict()))
            if isResponseParsed:
                return parseControllerResponse(data=False, statuscode=400, 
                message="Message Id Taken", 
                error="A message with the given message id already exists.", 
                )
            return False
        
        if isResponseParsed:
            return parseControllerResponse(data=False, statuscode=500, 
                message="Internal Server Error", 
                error="Something went wrong try again later", 
            )
        return False

    except AssertionError as err:
        if str(err) == "Invalid user":
            logging.debug("Cannot add message for the user because, \
                a user with the given discord handle {} doesn't exist".format(message.author))
            if isResponseParsed:
                return parseControllerResponse(data=False, statuscode=400, 
                message="Message author's discord handle is not registered", 
                error="A user with the given discord handle {} doesn't exist".format(message.author), 
                )
            return False
        # A active scrum doesn't exist
        # Ask user to start a scrum before starting a scrum
        # Make sure , only creating discussions is not possbible
        # bot shd be able to add replies even when no scrum is active
        logging.info("Tried to add a discussion before starting a scrum")
        if isResponseParsed:
            return parseControllerResponse(data=False, statuscode=400, 
            message="No active scrum", 
            error="Start a scrum before sending trying add a discussion.", 
            )
        return False

    except Exception as e:
        logging.error("Couldn't create the message {} due to, {}".format(message.dict(), e))
        if isResponseParsed:
            return parseControllerResponse(data=False, statuscode=500, 
            message="Internal Server Error", 
            error="Something went wrong try again later", 
            )
        return False

def _createNewDiscussionForScrum(message: CreateMessageSchema, author: MemberInDBSchema):

    try: 
        assert not message.isReply, "message is a reply"
        oldDiscussion = _findMessageInDBFromMesssageId(messageId=message.messageId)
        assert not oldDiscussion, "discussion already exists"

        newDiscussion = Message(messageId=message.messageId)
        newDiscussion.message = message.message
        newDiscussion.tags = message.tags
        newDiscussion.author = author.mongoDocument
        newDiscussion.replies = []
        
        newDiscussion.save()

        # add this message to scrum
        addMessageToScrum(message=newDiscussion)
        
        return MessageControllerHelper.Success

    except AssertionError as err:
        # caused when we improperly called for a reply
        if str(err) is "message is a reply":
            raise Exception("Tried to create a discussion for a reply, \
                for the message {}".format(message))
        return MessageControllerHelper.MessageIdTaken


    except Exception as e:
        logging.error("Couldn't create a new messsage for the scrum due to ", e)
        raise Exception("Couldn't create a new messsage for the scrum due to ", e)

def _createReplyForScrum(message: CreateMessageSchema, author: MemberInDBSchema):

    try:
        assert message.isReply , "not reply"
        parentMessage = _findMessageInDBFromMesssageId(messageId=message.parentMessage)
        assert parentMessage, "No parent message"
        newReply = Message(messageId=message.messageId)
        newReply.message = message.message
        newReply.author = author.mongoDocument
        newReply.replies = []
        newReply.save()
        if parentMessage.replies:
            parentMessage.replies.append(newReply)
        else:
            parentMessage.replies = [newReply]
        parentMessage.save()
        return MessageControllerHelper.Success

    except AssertionError as err :
        # caused when we improperly called for a discussion
        if str(err) == "not reply":
            logging.error("Tried to create a discussion for a reply, \
                for the message {}".format(message))
            return MessageControllerHelper.WrongFormat
        
        logging.debug("Couldn't add reply because the parent message \
            with the id : {} doesn't exist".format(message.parentMessage))
        return MessageControllerHelper.ParentMessageNotFound
        

    except Exception as e:
        logging.error("Couldn't create a new reply for the scrum due to ", e)
        raise Exception("Couldn't create a new reply for the scrum due to ", e)


def _findMessageInDBFromMesssageId(messageId: str):
    """Finds the message document from the given messageId, if 
    the message doesn't exist, None is returned"""

    try:
        messageInDB : Message = Message.objects(messageId=messageId).first()
        assert messageInDB
        return messageInDB

    except AssertionError as _:
        # no message exists with that Id
        return None
    except Exception as e:
        helpfulErrorMessage = "Couldn't find a the a message with the messageId : {}. Due to {}".format(messageId, e)
        logging.error(helpfulErrorMessage)
        raise Exception(helpfulErrorMessage)

def UpdateMessageInDatabase(message : UpdateMessageSchema, **kwargs):
    isResponseParsed = kwargs.get("isParsed", False)
    logging.info("Attempting to update the message with the data {}".format(message.dict()))
    try:
        oldMessage = _findMessageInDBFromMesssageId(message.messageId)

        # make sure the message exists
        assert oldMessage

        oldMessage.message = message.message
        oldMessage.tags = message.tags
        oldMessage.timeStamp = datetime.now()

        oldMessage.update()

        if isResponseParsed:
            return parseControllerResponse(data=True, statuscode=200,  
            message="Successfully updated the message")
        return True

    except AssertionError as _:
        # A message with the given message id doesn't exist
        # return 400
        logging.debug("Couldn't update the message with the message id : {} \
            as a message with the given message id was not found".format(message.messageId))
        
        if isResponseParsed:
            return parseControllerResponse(data=False, statuscode=400, 
            error="A message with the given messageId doesn't exist", 
            message="Invalid message id")
        return False
    
    except Exception as e:
        logging.error("Couldn't update the message : {} as the following error occurred {}".format(message, e))

        if isResponseParsed:
            return parseControllerResponse(data=False, statuscode=500, 
            error="Something went wrong, try again later", 
            message="Internal Server Error")
        return False
    
class MessageControllerHelper(Enum):
    """Helper enum for message creation"""
    Success = auto()
    MessageIdTaken = auto()
    UserNotFound = auto()
    ParentMessageNotFound = auto()
    WrongFormat = auto() # trying to create reply instead of discussion, vice-versa
    InternalServerError = auto()
