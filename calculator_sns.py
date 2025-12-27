import json
import operator
import logging
from typing import Callable

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
OPERATIONS: dict = {
    '*': operator.mul,
    '-': operator.sub,
    '+': operator.add,
    '/': operator.truediv
}

def getCalcData(event)->dict:
    try:
        calcData: dict = json.loads(event["Records"][0]["Sns"]["Message"])
    except  Exception:
        raise AttributeError("Wrong stricutre of SNS event") 
    return calcData  
def getOperation(calcData: dict) -> Callable[[float, float], float]:
    operation: dict = calcData["operation"]
    res:  Callable[[float, float], float] = OPERATIONS.get(operation) 
    if not res:
        raise ValueError(f"Wrong operation {operation}")
    return res     
     
def lambda_handler(event, __):
    logger.debug(f"received event {event}")
    calcData: dict = getCalcData(event)
    operationMethod = getOperation(calcData)
    print (operationMethod(calcData["op1"], calcData["op2"]))
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

