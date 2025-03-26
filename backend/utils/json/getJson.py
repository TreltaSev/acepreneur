import quart

from utils.exception import HighLevelException
from utils.types import Struct

def getJson(func):
    """
    Attempts to gather the json data from a :class quart.request: then it converts the dictionary into
    a hierarchial object, passes the object rhrough the parent function as an object as well as the dict
    as well.
    """
    async def wrap(*args, **kwargs):
        try:
            json: dict = await quart.request.json;
            if not json:
                raise TypeError("Json None")            
        except Exception as e:
            raise HighLevelException("Json Object Invalid", severity="Error", name="JsonParser")
        
        json_struct: Struct = Struct(**json)

        return await func(json=json, json_struct=json_struct, *args, **kwargs)
    return wrap


