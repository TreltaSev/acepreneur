import requests
import base64

from utils.types.oauth2 import SessionClient, UserClient
from utils.exception import HighLevelException
from utils.types import Struct
from utils.mongo import MongoClient

from typing import List, Callable

def getUser(cut: List[str] = ["access_token"]):
    """
    Attempts to automatically request the user data from mongo db.
    
    Parameters
    ----------
    `cut : List[str]`
        List of key values to cut or delete right before response
    
    
    Example Usage
    ```python
    @blueprint.route(rule="", methods=["GET"])
    @getHeaders(["Bearer"], explicit=True)
    @getUser()
    async def foo(headers, user):
        print(headers) # Struct Object, access headers.dict for dictionary
        print(user) # User Object
    ```
    """
    
    # Make sure access_token is NEVER accessible
    if "access_token" not in cut:
        cut.append("access_token")

    def decorator(func: Callable):
        
        async def wrap(*args, **kwargs):
            """
            Should access headers, get bearer token, try to locate user with said bearer token, then pass
            a user kwarg through to the child function
            """

            headers = kwargs.get("headers", None)

            # Check for headers
            if not headers:
                raise HighLevelException(
                    "Header not found in **kwargs",
                    dev_note="Did you use @getHeaders([\"Bearer\"]) on the function?",
                    name="getUser",
                    func=func.__name__,
                    status=400
                )

            # Check for Bearer Token
            if not hasattr(headers, "Bearer"):
                raise HighLevelException(
                    "Headers found the required \"Bearer\" header wasn't included...",
                    dev_note="User probably didn't sign in... or idk bug smth",
                    name="getUser",
                    func=func.__name__,
                    status=400
                )

            # Check if identification token corresponds to a session
            SessionSearch = MongoClient.sessions.find_one(
                {"token": headers.Bearer})

            if not SessionSearch:
                raise HighLevelException(
                    "User session wasn't found, this means the id token either is malformed, or it expired.",
                    dev_note="Try signing in...?",
                    name="getUser",
                    func=func.__name__,
                    status=401
                )

            UserSession = SessionClient(genTimes=False, **SessionSearch)

            if (UserSession.expired):
                MongoClient.sessions.delete_one({"token": headers.Bearer})
                raise HighLevelException(
                    "User session has expired, it was therefore deleted. Thank you, come again ~ apu",
                    dev_note="Sign in again :)",
                    name="getUser",
                    func=func.__name__,
                    status=402
                )

            # Assume user session isn't expired

            # Attempt to get user from user db using id
            UserSearch = MongoClient.users.find_one(
                {"id": UserSession.id, "provider": UserSession.provider})

            # Check if exists
            if not UserSearch:
                raise HighLevelException(
                    "User session was found but user in database wasn't...?",
                    dev_note="This should be a really really rare bug. I honestly dfk what could cause this other than an admin deleting things randomly",
                    name="getUser",
                    func=func.__name__,
                    status=401
                )

            UserData = UserClient(**UserSearch)

            if UserData.provider == "microsoft":
                # Get User Pfp
                headers = {
                    'Authorization': f'Bearer {UserData.access_token}',
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }


                response = requests.get(f"https://graph.microsoft.com/v1.0/me/photo/$value", headers=headers)

                if response.ok:                
                    mime_type = response.headers.get('Content-Type', 'application/octet-stream')
                    image_b64 = base64.b64encode(response.content).decode("utf-8")
                    data_uri = f"data:{mime_type};base64,{image_b64}"
                    UserData.profile = data_uri
                    
            if UserData.provider == "local":
                response = requests.get("https://i.ibb.co/P6f8yYP/default-avatar-profile-icon-of-social-media-user-vector-1.png")
                
                mime_type = response.headers.get("Content-Type", "application/octet-stream")
                image_b64 = base64.b64encode(response.content).decode("utf-8")
                data_uri = f"data:{mime_type};base64,{image_b64}"
                UserData.profile = data_uri
            
            for k in cut:
                if hasattr(UserData, k):
                    delattr(UserData, k)
                    
            return await func(user=UserData, *args, **kwargs)
        return wrap
    return decorator
