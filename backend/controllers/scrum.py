import logging

from models.scrum import Scrum
from app.helper import parseControllerResponse

def createScrum():
    """Creates a scrum and returns the its object id"""
    
    # * Note: make sure to check there is no active scrum,
    #         before calling create scrum
    #
    # * Also need to set active scrum to the created scrum id

    try:
        newScrum = Scrum()
        newScrum.name = newScrum.generateName()
        newScrum.messages = []
        newScrum.save()
        
        resp = {
            "scrumId" : newScrum.id.__str__(),
            "scrumName": newScrum.name
        }

        parseControllerResponse(data=resp, statuscode=200, message="Scrum Created")

    except Exception as e:
        logging.error("Couldn't create a scrum due to ", e)
        raise Exception("Couldn't create a scrum due to ", e)

def findScrumNameWithTheGivenId(id: str):
    """Finds the scrum with the given id"""

    try:
        [scrum] = Scrum(id=id)

        resp = {
            "scrumName": scrum.name
        }

        parseControllerResponse(resp, statuscode=200, message="Scrum Found")

    except Exception as e:
        logging.error("Couldn't find the scrum with the id : {}. Due to".format(id), e)
        raise Exception("Couldn't find the scrum with the id : {}. Due to".format(id), e)