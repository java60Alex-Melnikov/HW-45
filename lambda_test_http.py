import json
import boto3
import logging
import os
from validation.src.pydantic_validation import validate
from validation.src.calculator_data import CalculateData

logger = logging.getLogger()
logger.setLevel(os.getenv("LOGGING_LEVEL", logging.DEBUG))

def __response(code, body):
    return {
        'statusCode': code,
        'body': json.dumps(body)
    }

def __publishData(data: CalculateData) -> tuple[int, dict]:
    dataJSON = data.model_dump_json()
    logger.debug(f"publishing {dataJSON}")
    sns = boto3.client("sns", region_name="il-central-1")
    topicArn = "arn:aws:sns:il-central-1:436705618119:calculator-topic"
    code: int = 500
    body = {}

    try:
        response = sns.publish(TopicArn=topicArn, Message=dataJSON)
        logger.debug(f"response from sns is {response}")
        body = {"messageId": response["MessageId"]}
        code = 200

    except Exception as e:
        logger.error(f"error publishing {dataJSON}, error is {e}")
        body = {"detail": str(e)}
        code = 500 
    
    logger.debug(f"from publishing: code={code}, body = {body}")
    return code, body       
           
def __calculationProcessing(dataJSON: str):
    logger.debug(f"processing {dataJSON}")
    code: int = 400
    body: dict = {}
    try: 
        calcData = validate(CalculateData, dataJSON)
        logger.debug(f"validated data is {calcData}")
        code, body = __publishData(calcData)
        
    except Exception as e:
        logger.error(f"Processing error: {e}")
        body = {"detail": str(e)}
        code = 400
        
    return code, body
    
def lambda_handler(event, __):
    logger.debug(f"event is {event}")
    rawPath = event.get("rawPath", "")
    code: int = 404 
    body = f"{rawPath} not found"
    
    if "/health" in rawPath:
        code = 200
        body = {"status": "up"}
    elif "/calculation" in rawPath:
        requestBody = event.get("body", "{}")
        logger.debug(f"body in request is {requestBody}")
        code, body = __calculationProcessing(requestBody) 
        logger.debug(f"in response body {body}, code {code}")
        
    return __response(code, body)
