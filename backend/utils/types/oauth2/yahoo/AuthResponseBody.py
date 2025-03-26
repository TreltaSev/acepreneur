from utils.types import Struct

class AuthResponseBody(Struct):    
    sub: str
    name: str
    given_name: str
    family_name: str
    nickname: str
    locale: str
    email: str
    email_verified: bool
    profile_images: dict
    picture: str

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)