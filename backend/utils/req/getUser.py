from utils.exception import HighLevelException
from utils.types import User
from utils.mongo import MongoClient

from typing import List, Callable

def getUser(*args, **kwargs):
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
            UserSearch = MongoClient.users.find_one(
                {"id": headers.Bearer})

            if not UserSearch:
                raise HighLevelException(
                    "User session wasn't found, this means the user-id might be malformed...",
                    dev_note="Try restarting the app?",
                    name="getUser",
                    func=func.__name__,
                    status=401
                )

            user = User(**UserSearch)
                    
            return await func(user=user, *args, **kwargs)
        return wrap
    return decorator
