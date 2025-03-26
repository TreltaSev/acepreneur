from utils.types import Struct

class AuthResponseBody(Struct):    
    userPrincipalName: str
    id: str
    displayName: str
    surname: str
    givenName: str
    preferredLanguage: str
    mail: str

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)