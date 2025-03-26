import requests
import base64

from utils.types.oauth2 import SessionClient, UserClient
from utils.exception import HighLevelException
from utils.types import Struct
from utils.mongo import MongoClient

from utils.types.finance import FinanceUserClient

def getUserFinance(func):
    """
    Attempts to automatically request the user data from mongo db.

    Example Usage
    ```python
    @blueprint.route(rule="", methods=["GET"])
    @getHeaders(["Bearer"], explicit=True)
    @getUser
    async def foo(headers, user):
        print(headers) # Struct Object, access headers.dict for dictionary
        print(user) # User Object
    ```
    """
    async def wrap(*args, **kwargs):
        user = kwargs.get("user", None)
        
        if not user:
            raise HighLevelException(f"No user object found, passed through {func.__name__}")
        
        # Attempt to get user from user db using id
        UserSearch = MongoClient.users.find_one(
            {"id": user.id, "provider": user.provider})
        
        financeUser = FinanceUserClient()

        return await func(user=, *args, **kwargs)

    return wrap
