import os
import boto3
from botocore.exceptions import ClientError
import logging
import json
CLIENT_ID = "6n5mvgjg3rje55ek2dtkju0tmm"

AUTH_RESULT ="AuthenticationResult"
ACCSESS_TOKEN = "AccessToken"
ID_TOKEN = "IdToken"
logger = logging.getLogger("lambda_function")
logger.setLevel(os.getenv("LOGGING_LEVEL", logging.INFO))
def getRefreshToken(event)-> str:
    bodyJSON = event.get("body", "{}")
    res: str = ""
    try:
        body = json.loads(bodyJSON)
        res = body["refreshToken"]
    except Exception:
        pass
    return res    
def initiate_auth(client, refreshToken)->dict:
    resp = client.initiate_auth(
        AuthFlow="REFRESH_TOKRN_AUTH",
        ClientId = CLIENT_ID,
        AuthParameters ={
            "REFRESH_TOKEN":refreshToken
        }
    )
    return resp

def refreshProcessing(client, refreshToken):
    code = 400
    body = {"error": "No refresh token"}   
    if refreshToken:
        try:
            resp = initiate_auth(client, refreshToken)
            code = 200
            body = getAuthResBody(resp)
        except ClientError as ce:
            errorObj = ce.response.get("Error") 
            if not errorObj:
                code = 500
                body = {"error": f"Unknown error: {ce.response}"}  
            else:
                body = {"error": errorObj["Message"]} 
    return __response(code, body)                
   


                   
def __response(code, body):
    return {
        'statusCode': code,
        'body': json.dumps(body)
    } 



def getAuthResBody(resp) -> dict:
    authRes = resp[AUTH_RESULT]
    body = {
                "access_token":authRes[ACCSESS_TOKEN],
                "id_token": authRes[ID_TOKEN],
            } 
    return body     

def debugAuthResp(resp):
    authRes = resp.get(AUTH_RESULT)
    return authRes[ACCSESS_TOKEN][:10] 

def lambda_handler(event, __):
    logger.debug("event is %s", event)
    client = boto3.client("cognito-idp", region_name="il-central-1")
    refreshToken = getRefreshToken(event)
    return refreshProcessing(client, refreshToken)
          

 