import quart
from pathlib import Path
import importlib.machinery
from siblink import Config
from typing import Any, Callable, List, Union
from utils.exception import HighLevelException
from utils.package import cloakquart
from pyucc import console
import re
import traceback

class Blueprint(quart.Blueprint):
  """
  Inherited from :class:`quart.Blueprint`, contains customized logic for easier error handling
  and cleaner code :) just dont look to far under the hood...  
  """

  def __init__(self, *args: Any, **kwargs: Any) -> None:
    super().__init__(*args, **kwargs)

  def route(self, rule: str, **options: Any) -> Any:
    """
    Shadows `quart`'s `quart.Blueprint` route class method which allows the possibility of customizable and automatic
    error handling, rate limiting, and possibly server caching and logging. just like `quart`'s `quart.Blueprint.route()` decorator,
    this decorator calls :func:`add_url_rule` but unlike the vanilla `quart.Blueprint.route()` decorator, this method has an entry point
    to the before execution of the designated method. While inserting execution is possible, as of right now on rewrite@v1.1, the method is locked
    to doing basic error handling with the :class:`HighLevelException` class.

    ``` code-block:: python
      bp: cloakquart.Blueprint = cloakquart.Blueprint("test-bp", __name__)

      # This can be used as quart.Blueprint would.
      @bp.route(rule="/", methods=["GET"])
      def root():
        return ":)"
    ```


    """
    def decorator(f: Callable) -> Callable:
      """
      Since quart.Blueprint.route is a decorator, this also needs to be a decorator. this can be called a wrapper interchangeably as well.
      This decorators sole purpose is to replicate and execute the same logic as @quart.Blueprint.route() while also automatically
      adding "before" logic. meaning logic that is literally ran before the main call (like error handling seen here). 

      As of :version:`v1.1` this logic is predetermined to be error handling but that doesn't mean that it can stop here.

      :arg f: typing.Callable: Function or method, any callable object. Starts decorator logic.
      """

      async def modified(*args, **kwargs):
        """
        This is a modified asynchronous method that is assigned to the url rule that is executed 
        whenever this decorator is reached. Whatever this method does is whatever is basically responded to 
        within the backend server. The only difference is that here, error handling is automatically attached to the main
        logic of whatever method the decorator hooks to.
        """
        # Run any before scripts or sections
        # HERE

        # Child Starting
        try:
          result = await f(*args, **kwargs)
          return result
        except Exception as error:
          if hasattr(error, "json"):
            error: HighLevelException
            return error.json
          console.fail(f"Error @ {f.__code__}")
          traceback.print_exc()
          return HighLevelException(f"Unregistered Error within {f.__name__}", name="Blueprint.py").json

      endpoint = options.pop("endpoint", None)
      self.add_url_rule(rule, endpoint, modified, **options)
      return modified

    return decorator

  def refactor_route(self, rule: str, **options: Any):
    """
    Creates a working Quart.Route and allows for different functions for each individual method. Instead of having multiple
    if statements to check which logic you should run, create an object using this method, and use that object.
    This method has similar input args as :method:`Blueprint.route` and has very similar functionality. This method returns a :class:`cloakquart.Route` object.
    This object contains a :method:`Route.on()` decorator method. This decorator can be used to split your quart routes.

    ```python

    route = blueprint.refactor_route("/dev/test_route", methods=["GET", "POST"])

    @route.on("GET")
    def route_GET(*args, **kwargs):
      print(quart.request.method) # GET
      return "Hello" 

    @route.on("POST") 
    def route_POST(*args, **kwargs):
      print(quart.request.method) # POST
      return "POST HELLO"
    ```
    """
    route = cloakquart.RefactoredRoute(rule, **options)
    endpoint = options.pop("endpoint", None)
    self.add_url_rule(rule, endpoint, route.execute, **options)
    return route  


  @classmethod
  @Config.load_config
  def __get_blueprints__(cls) -> List[Union[importlib.machinery.ModuleSpec, str]]:
    """
    Gathers all blueprints that are registered within the config.json file (possibly the ./defaults/backend.default.json file)
    these blueprint values are formatted and converted into a mutable Path object. This object is then checked to see if it exists,
    if it doesn't raises an :error:`FileNotFound` Error.
    This object is then reformatted again, replacing each "/" and "\\" with "." and removing the end path, basically
    converting it into a ModuleSpec object and appended into variable which this function will return.
    :returns: List[Union[importlib.machinery.ModuleSpec, str]]: List of spec objects which can be inserted into :method:`cloakquart.Quart.load`
    """
    out_specs: List[Path] = []
    
    api: Path = Config.root / "api"
    
    files = api.rglob("*.py")
    
    for file in files:      
      
      # Skip files starting with _
      if file.name.startswith('_'):
        continue
      
      # Save if conditions passed
      if not any(part.startswith("_") for part in file.parts):
        out_specs.append(str(file).replace("/", ".").replace("\\", ".").replace(".py", ""))
      
    return out_specs