from utils.exception import HighLevelException
from utils.types import User, Severity
from utils.mongo import MongoClient
from utils.types import Struct

from typing import List, Callable

def requireAdmin(*args, **kwargs):
    """
    Prevents Unauthorized access
    
    
    Example Usage
    ```python
    @blueprint.route(rule="", methods=["GET"])
    @getHeaders(["Bearer"], explicit=True)
    @getUser()
    @requireAdmin
    async def foo(headers, user):
        print(headers) # Struct Object, access headers.dict for dictionary
        print(user) # User Object
    ```
    """

    def decorator(func: Callable):
        
        async def wrap(*args, **kwargs):

            user: Struct | None = kwargs.get("user", None)

            # Check if user is specified
            if not user:
                raise HighLevelException("Missing User from calling function, did you call @getUser()?")
            
            # Check if the user is admin
            is_admin = user.get("admin", False)
            if not is_admin:
                raise HighLevelException("You don't have the required permissions to access this... Missing: Administrator", severity=Severity.Error)
            
            # Continue Calling the child function
            return await func(*args, **kwargs) 
        return wrap
    return decorator
