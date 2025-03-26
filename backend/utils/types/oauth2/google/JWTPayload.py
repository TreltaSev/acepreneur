from utils.types import Struct


class JWTPayload(Struct):    
    iss: str
    azp: str
    aud: str
    sub: str
    email: str
    email_verified: bool
    nbf: str
    name: str
    picture: str
    given_name: str
    family_name: str
    iat: int
    exp: int
    jti: str

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)