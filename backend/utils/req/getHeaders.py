import quart

from utils.exception import HighLevelException
from utils.types import status, Struct
from typing import List, Callable

def getHeaders(headers: List[str] | str, explicit: bool = False):
    """
    Gets the available headers from an http request.

    ### Example Usage
    ```python
    @blueprint.route(rule="", methods=["GET"])
    @getHeaders(["Bearer"], explicit=True)
    def exampleRoute(headers: Struct):
        print(headers.dict)
    ```

    :param headers: Headers that will be passed back down to the child function
    :type headers: List[str] | str
    :param bool explicit: Determines wether or not to raise an error if a header isn't
    found.
    """

    # Convert String to List
    if isinstance(headers, str):
        headers = [headers]

    def decorator(f: Callable) -> Callable:       

        async def wrap(*args, **kwargs):
            response_headers = {} # Empty

            for header in headers:

                # Get Header
                header_value = quart.request.headers.get(header)
                
                # Conditional Check for None
                if not header_value and explicit:
                    raise HighLevelException("Failed to locate header", status=400)
                
                # Save
                response_headers[header] = header_value

            return await f(headers=Struct(**response_headers), *args, **kwargs)
        
        return wrap
    return decorator