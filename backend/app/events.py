from typing import Callable
import os

from fastapi import FastAPI

from .database import createConnection, closeConnection

def createStartAppHandler(app: FastAPI):
    async def startApp():
        createConnection()
    
    return startApp

def createStopAppHandler(app: FastAPI):
    def closeApp():
        closeConnection()

    return closeApp