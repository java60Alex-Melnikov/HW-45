import os
from validation.src.pydantic_validation import validate
from login_data import LoginData
CLIENT_ID = "3c9viqd9tt0jrghfogm3t1a0gi"
CHALLENGE_NAME_PROP = 'ChallengeName'
CHALLENGE_NAME_VALUE = "NEW_PASSWORD_REQUIRED"
AUTH_RESULT ="AuthenticationResult"
ACCSESS_TOKEN = "AccessToken"
REFRESH_TOKEN = "RefreshToken"
ID_TOKEN = "IdToken"
AUTH_ERROR_CODE = "NotAuthorizedException"
ERROR_MESSAGE = "Incorrect username or password"
PASSWORD_NOT_MATH_POLICY = "InvalidPasswordException"
def initiate_auth(client, username, password)->dict:
    resp = client.initiate_auth(
        AuthFlow="USER_PASSWORD_AUTH",
        ClientId = CLIENT_ID,
        AuthParameters ={
            "USERNAME":username,
            "PASSWORD": password
        }
    )
    return resp

def respond_to_new_passowrd_challenge(client, username, password, session) -> dict:
    resp = client.respond_to_auth_challenge(
        ClientId = CLIENT_ID,
        ChallengeName = CHALLENGE_NAME_VALUE,
        Session = session,
        ChallengeResponses = {
            "USERNAME":username,
            "NEW_PASSWORD": password
        }
    )
    return resp
   
import logging
import json
logger = logging.getLogger("lambda_function")
logger.setLevel(logging.DEBUG)
                   
def __response(code, body):
    return {
        'statusCode': code,
        'body': json.dumps(body)
    } 
def getCredentials(event) -> LoginData:
    bodyJson = event.get("body", "{}")
    try:
        return validate(LoginData, bodyJson)
    except Exception as e:
        logger.error(f"Validation failed: {e}")
        return None  
     
def wrong_resp(): 
    return __response(400, {"error": ERROR_MESSAGE})
def processNewPasswordFlow (client, username:str, newPassword: str | None, respCognito)->tuple[int, dict]:
    code: int = 400
    body: dict  = {"error": "New Password should be provided"}
    if newPassword:
        resp = respond_to_new_passowrd_challenge(client=client, username=username, password=newPassword,
                                          session=respCognito.get("Session"))
        logger.debug("from new passowrd response: %s", debugAuthResp(resp))
        code = 200
        body = getAuthResBody(resp)
    return code, body 
            
        
    
        
def authenticate(client, username: str, password: str, newPassword: str | None) :
    try:
        code = 500
        body ={"error":"Unprocessed block"}
        resp = initiate_auth(client, username, password)
        logger.debug("response from initiate_auth is %s ...",
                    debugAuthResp(resp))
        if AUTH_RESULT in resp:
            code = 200
            body = getAuthResBody(resp)
        else:
            code, body = processNewPasswordFlow(client, username, newPassword, resp) 
    except  ClientError as ce:
        errorObj = ce.response.get("Error", {})
        errorCode = errorObj.get("Code", "")
        if errorCode == AUTH_ERROR_CODE:
            code = 400
            body = {"error": ERROR_MESSAGE}
        elif errorCode == PASSWORD_NOT_MATH_POLICY:
            code = 400
            body = {"error": errorObj.get("Message")}    
        else:
            code = 500
            body = {"error": f"Unknown error {str(ce)}"}    
    except Exception as e:
        body = {"error": f"Unknown error {str(e)}"}        
    return __response(code, body) 

def getAuthResBody(resp) -> dict:
    authRes = resp[AUTH_RESULT]
    body = {
                "access_token":authRes[ACCSESS_TOKEN],
                "id_token": authRes[ID_TOKEN],
                "refresh_token": authRes[REFRESH_TOKEN]
            } 
    return body     

def debugAuthResp(resp):
    authRes = resp.get(AUTH_RESULT)
    return authRes[ACCSESS_TOKEN][:10] if authRes else resp[CHALLENGE_NAME_PROP]

def lambda_handler(event, __):
    logger.debug("event is %s", event)
    client = boto3.client("cognito-idp", region_name="il-central-1")
    login_data = getCredentials(event)
    
    if login_data:
        return authenticate(client, login_data.username, login_data.password, login_data.newPassword)
    else:
        return wrong_resp()