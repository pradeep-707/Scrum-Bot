from mongoengine import connect, disconnect
import logging

from .config import MONGO_URI

def createConnection():
    connect(host=MONGO_URI)
    logging.info("Connected to the database %s", MONGO_URI)

def closeConnection():
    disconnect()
    logging.info("Disconnected from the database %s", MONGO_URI)