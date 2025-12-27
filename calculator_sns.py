import json
import operator
import logging
import os
from typing import Callable
from validation.src.pydantic_validation import validate
from validation.src.calculator_data import CalculateData

logger = logging.getLogger()
logger.setLevel(os.getenv("LOGGING_LEVEL", logging.DEBUG))

OPERATIONS: dict = {
    '*': operator.mul,
    '-': operator.sub,
    '+': operator.add,
    '/': operator.truediv
}

def getCalcData(event) -> CalculateData:
    try:
        message_json = event["Records"][0]["Sns"]["Message"]
        return validate(CalculateData, message_json)
    except Exception as e:
        logger.error(f"Validation error: {e}")
        raise AttributeError("Wrong structure of SNS event or validation failed") from e

def getOperation(calcData: CalculateData) -> Callable[[float, float], float]:
    operation: str = calcData.operation
    res: Callable[[float, float], float] = OPERATIONS.get(operation)
    if not res:
        raise ValueError(f"Wrong operation {operation}")
    return res

def lambda_handler(event, __):
    logger.debug(f"received event {event}")
    try:
        calcData: CalculateData = getCalcData(event)
        operationMethod = getOperation(calcData)
        result = operationMethod(calcData.op1, calcData.op2)
        print(f"Result: {result}")
        return {
            'statusCode': 200,
            'body': json.dumps(f"Result: {result}")
        }
    except Exception as e:
        logger.error(f"Error processing event: {e}")
        print(f"Error: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps(str(e))
        }