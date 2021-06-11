from mongoengine import connect
import logging


def connectDb(mongoUri):
    connect(host=mongoUri)
    logging.info("Connected to the database %s", mongoUri)
