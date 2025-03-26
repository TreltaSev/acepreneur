import quart
import functools
from utils.exception import HighLevelException
from typing import List, Any, Union, Literal, Callable


undef = type("-", (), {})


class ParsedJson(dict):
  def __init_subclass__(cls) -> None:
    return super().__init_subclass__()

  def set(self, query, value: Any):
    """
    Sets the value according to :val:`value` at position :val:`query`
    query can be something like user.password and its usage would be:

    ``` python
    dict: ParsedJson({"user": {}})
    dict.set("user.password", value)
    ```
    """

    query = query.split(".")

    step = self

    # Loop through query
    for index, c in enumerate(query):

      # Index starts at 0, length starts at 1.
      is_end = (index + 1) == len(query)

      # Create a parent within dictionary if needed
      if c not in step and not is_end:
        step[c] = {}

      # Handle value assignment
      if is_end:
        if not isinstance(step, dict):
          raise TypeError(f"Segment in query is not object, is {type(step)} instead.")
        step[c] = value
        break

      step = step[c]

  def get(self, query, default: Any = undef):
    """
    Return the value for key if key is in the dictionary, else default.
    :val:`query` is the string
    that will be used to determine where it will look.
    Query might look something like user.password and it would return true
    if the dict looked like this:

    ``` python
    dict: dict = {
      "user": {
        "password": 312
      }
    }
    """
    query = query.split(".")

    step = self
    for c in query:
      try:
        step = step[c]
      except Exception:
        if default is not undef:
          return default
        raise HighLevelException(f"Key not found: {query}")
    return step

  def has(self, query: str):
    """
    Checks if the dict has a key within it, :val:`query` is the string
    that will be used to determine where it will look.
    Query might look something like user.password and it would return true
    if the dict looked like this:

    ``` python
    dict: dict = {
      "user": {
        "password": 312
      }
    }
    ```
    """
    query = query.split(".")

    step = self
    for c in query:
      try:
        step = step[c]
      except Exception:
        return False
    return True


def parseJson(accepted: Union[Literal[True], List[str]] | Callable = True):
  """
  Decorator that automatically attempts to parse a json request object.
  When used as a decorator, this method will inject a object within the kw arguments
  of the child function, the object that it would inject is :return:`jRequest`
  if :var:`accepted` is not true and is instead a list containing strings :return:`jRequest` will only 
  "accept" values that are in the accepted list. Any other value will be ignored.
  """
  def decorator(f: Callable):
    @functools.wraps(f)
    async def wrap(*args, **kwargs):
      try:
        # Sanitize unwanted keys
        jRequest = {}
        request_json: dict = await quart.request.json
        if accepted == True or callable(accepted):
          jRequest = request_json
        else:
          for k, v in request_json.items():
            if k in accepted:
              jRequest[k] = v

        # Check if data is valid json
        if not isinstance(jRequest, dict):
          raise TypeError
      except Exception as e:
        raise HighLevelException("Failed to parse JSON", payload=str(await quart.request.get_data(as_text=True)))
      return await f(jRequest=ParsedJson(jRequest), *args, **kwargs)
    return wrap
  if callable(accepted):
    return decorator(accepted)
  return decorator