from utils.types import Struct
from typing import Literal
import datetime


class SessionClient(Struct):
    """
    Stores relevant information for user sessions, including a unique identifier linking
    to the users information in the :database.users: collection and a unique identification
    token.

    ## Usage
    ```python
    ClientData: dict = {"provider": "Google", "id": "", "token": ""}
    SessionData = SessionClient(**ClientData)
    SessionData.dict # Dictionary Representation
    ```

    :param provider: Provider, i.e. api used for sign in. Valid providers include
    "Google", "Microsoft", "Yahoo", and "FinalFinance"
    :type provider: Literal["Google", "Microsoft", "Yahoo", "FinalFinance"]
    :param str id: Customer/Client full name
    :param str token: Identification token
    :param int expires: [Optional, Created on init] Unix Timestamp of when session should be expired
    :param int created: [Optional, Created on init] Unix Timestamp of when session was created
    """

    def __init__(self, genTimes: bool = True, **kwargs) -> None:
        # Type Annotation
        self.provider: Literal["Google", "Microsoft", "Yahoo", "FinalFinance"]
        self.id: str
        self.token: str
        self.expires: int
        self.created: int

        if genTimes:
            # Get Unix Timestamps for self.expires and self.created
            self.determineTimes()

        super().__init__(**kwargs)

    def determineTimes(self):
        """
        Generates Unix time stamps for the current time as well as when
        the session should expire
        """
        created = datetime.datetime.now()
        expires = created + datetime.timedelta(hours=6)
        self.__dict__.update({
                "created": created.timestamp(),
                "expires": expires.timestamp()
            }
        )

    @property
    def expired(self) -> bool:
        """
        Checks the unix times to see if the user should be deleted...
        """
        now = datetime.datetime.now()
        expires = datetime.datetime.fromtimestamp(self.expires)
        return now > expires
