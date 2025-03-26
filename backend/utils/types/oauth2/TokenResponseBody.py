from utils.types import Struct


class TokenResponseBody(Struct):    
    access_token: str
    id_token: str
    expires_in: int
    token_type: str
    refresh_token: str
    xoauth_yahoo_guid: str


    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)