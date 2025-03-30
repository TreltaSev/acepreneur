import quart
from typing import Callable
from pyucc import colors, symbols, console
from utils.logger import Logger
from utils.types import Severity
from utils.exception import HighLevelException
from typing import List
import traceback


class RefactoredRoute:
  """
  Cloakquart Route Class used for refactored routes
  """

  def __init__(self, rule, **options) -> None:
    self.rule = rule
    self.options = options
    self.handlers = {
        "GET": None,
        "HEAD": None,
        "POST": None,
        "PUT": None,
        "DELETE": None,
        "CONNECT": None,
        "OPTIONS": None,
        "TRACE": None,
        "PATCH": None
    }

    for request_type in self.handlers.keys():
      if request_type not in options.get("methods", {}):
        self.handlers[request_type] = False

  def on(self, method: str | List[str]):
    """
    Register a method to a HTTP request type, works with :method:`cloakQuart.Blueprint.refactor_route()`
    """

    if isinstance(method, str):
      method = [method]
    
    method = [item.upper() for item in method]

    def decorator(f: Callable, **options):
      for i in method:
        if i not in self.handlers:
          Logger.__log__(f"\"{method}\" is not a valid http method for {colors.vibrant_blue}{self.rule}", Severity.Error)
          quit()

        handler_function = self.handlers.get(i)

        if handler_function is not None:
          Logger.__log__(f"Duplicate \"{i}\" http request register found for {colors.vibrant_blue}{self.rule}{symbols.reset}, ignoring.")

        self.handlers[i] = f

    return decorator

  async def execute(self, *args, **kwargs):
    """
    Modified async method that does exactly what quart.Route does but factors in refactored routes.
    """
    method = quart.request.method
    f = self.handlers.get(method, None)

    if f is None:
      return HighLevelException(f"\"{method}\" is a accepted request type but its not registered on this route.", Severity.Error, "Not Registered").json

    try:
      result = await f(*args, **kwargs)
      return result
    except Exception as error:
      if hasattr(error, "json"):
        error: HighLevelException
        return error.json, 400
      console.fail(f"Error @ {f.__code__}")
      traceback.print_exc()
      return HighLevelException(f"Unregistered Error within {f.__name__}", name="RefactoredRoute.py").json, 512