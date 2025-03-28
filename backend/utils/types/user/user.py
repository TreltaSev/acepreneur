from utils.types import Struct
from typing import Literal

class User(Struct):
    """
    Object used to store user data
    
    ## Usage
    ```python
    data: dict = {"id": "user-idhjwa...", "name": "trelta sebastion", likes: ["event-hjwidhoawi", "program-ouidwaod"]}
    user: User = User(**data) || User(data)
    user.dict # Dictionary Representation
    ```
    
    :param str id: User Id, starts with user-*
    :param str name: User given name, full name. Like "John Doe"
    :param likes: List of objects user has liked
    :type likes: List[str]
    """
    
    def __init__(self, obj=None, **kwargs):
        # __ Type Annotation __
        self.id: str | None
        self.name: str
        self.likes: str
        
        super().__init__(obj, **kwargs)
        
        # __ Create Defaults __
        self.__defaults()
        
    def __defaults(self):
        """
        Sets the defaults for this object
        """
        self.dict.setdefault("id", None)
        self.dict.setdefault("name", "User Name")
        self.dict.setdefault("likes", [])
