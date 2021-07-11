from typing import Callable
import os

from fastapi import FastAPI

from .database import createConnection, closeConnection
from controllers.constants import initConstants


def createStartAppHandler(app: FastAPI):
    async def startApp():
        createConnection()
        initConstants()

    return startApp


def createStopAppHandler(app: FastAPI):
    def closeApp():
        closeConnection()

    return closeApp
