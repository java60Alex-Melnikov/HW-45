import logging
import os

from calculator_data import CalculateData
from pydantic_validation import validate

def lambda_handler(event, __):
    logger = logging.getLogger("app")
    logger.setLevel(os.getenv("LOGGER_LEVEL", logging.DEBUG))
    logger.debug("event %s", event)
    messageJSON = event["Records"][0]["Sns"]["Message"]
    messageObj = validate(CalculateData, messageJSON)
    logger.info("message object %s", messageObj)