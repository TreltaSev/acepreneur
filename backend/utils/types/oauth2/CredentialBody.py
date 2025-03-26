from utils.types import Struct
from typing import Literal

class CredentialBody(Struct):
    """
    :param str email: Customer/Client email
    :param str hashed: Hashed Password
    :param str salt: Password Salt
    :param str id: Identifier, may not be accessible.
    """

    def __init__(self, **kwargs) -> None:
        # Type Annotation
        self.email: str
        self.hashed: str
        self.salt: str
        self.id: str

        super().__init__(**kwargs)