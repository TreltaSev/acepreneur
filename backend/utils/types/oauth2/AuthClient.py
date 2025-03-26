from utils.types import Struct
from typing import Literal

class AuthClient(Struct):
    """
    Object to be used across providers for a universal auth client object for
    easy type annotation and management.
    Uses the :class utils.types.Struct: class for easier management

    ## Usage
    ```python
    ClientData: dict = {"provider": "Google", "name": "", "email": "", "profile": "", "id: ""}
    AuthData = AuthClient(**ClientData)
    AuthData.dict # Dictionary Representation
    ```
    
    :param provider: Provider, i.e. api used for sign in. Valid providers include
    "Google", "Microsoft", "Yahoo", and "FinalFinance"
    :type provider: Literal["Google", "Microsoft", "Yahoo", "FinalFinance"]
    :param str name: Customer/Client full name
    :param str email: Customer/Client email
    :param str profile: A Url or Data object that contains the user's pfp
    :param str id: Identifier, may not be accessible.
    """

    def __init__(self, **kwargs) -> None:
        # Type Annotation
        self.provider: Literal["google", "microsoft", "yahoo", "local"]
        self.name: str
        self.email: str
        self.profile: str
        self.id: str

        super().__init__(**kwargs)