from utils.types import Struct
from siblink import Config


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
        self.__handle_admin(**kwargs)

    def __defaults(self):
        """
        Sets the defaults for this object
        """
        self.dict.setdefault("id", None)
        self.dict.setdefault("name", "User Name")
        self.dict.setdefault("likes", [])

    def __handle_admin(self, **kwargs):
        """
        Checks if the user should have admin access
        """
        headers: Struct = kwargs.get("headers", Struct({}))

        if not headers.has("Admin-Token"):
            return

        if headers.get("Admin-Token") == Config.admin.secret:
            self.dict["admin"] = True
