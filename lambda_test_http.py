import json
import boto3
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
number = (int, float)
schema: dict = {
    "op1": number,
    "op2": number,
    "operation": str
}
def __validateFields(data: dict, schema: dict):
    logger.debug(f"validating {data} with schema {schema}")
    for field, expType in schema.items():
        logger.debug(f"validating {field} with type {expType}")
        if field not in data:
            logger.error(f"Missing {field}")
            raise ValueError(f"Missing {field}")
        if not isinstance(data[field], expType):
            raise ValueError(f"Invalid type of {field}, should be a \
                             {'number' if isinstance(expType, tuple) else expType.__name__}")
    logger.debug(f"{data} is valid")                         
def __response(code, body):
    return {
        'statusCode': code,
        'body': json.dumps(body)
    }
def __publishData(dataJSON: str) -> tuple[int, dict]:
    logger.debug(f"publishing {dataJSON}")
    sns = boto3.client("sns", region_name="il-central-1")
    topicArn = "arn:aws:sns:il-central-1:436705618119:calculator-topic"
    code:int=None
    body = {}
    try:
        response = sns.publish(TopicArn=topicArn, Message=dataJSON)
        logger.debug(f"response from sns is {response}")
        body = {"messageId":response["MessageId"]}
        code = 200
    except Exception as e:
        logger.error(f"error publishing {dataJSON}, error is {e}")
        body = {"detail": str(e)}
        code = 500 
    logger.debug(f"from publishing: code={code}, body = {body}")
    
    return code, body       
           
def __calculationProcessing(dataJSON:str):
    logger.debug(f"processing {dataJSON}")
    code: int = 400
    body: dict = {}
    try: 
        data = json.loads(dataJSON)
        logger.debug(f"parsed data is {data}")
        __validateFields(data, schema)
        code, body = __publishData(dataJSON)
    except ValueError as ve:    
        body = {"detail": str(ve)}
    except Exception as e:
        body = {"detail": str(e)}
    return code, body
    
def lambda_handler(event, __):
    rawPath = event["rawPath"]
    logger.debug(f"raw path is {rawPath}")
    logger.debug(f"event is {event}")
    code:int = 404 
    body = "{rawPath} not found"
    if "/health" in rawPath  :
        code = 200
        body = {"status": "up"}
    elif "/calculation" in rawPath:
        requestBody = event["body"]
        logger.debug(f"body in request is {requestBody}")
        code, body = __calculationProcessing(requestBody) 
        logger.debug(f"in response body {body}, code {code}")   
    return __response(code, body) 
