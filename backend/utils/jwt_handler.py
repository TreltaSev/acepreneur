import json
import sys
import traceback
import jwt
import jwt.algorithms
import requests
import base64
from typing import Literal

from utils.types import Struct
from utils.types.oauth2.google import JWTPayload

class jwtHandler:

    # Google's public key url
    PublicKeyUrl: str = "https://www.googleapis.com/oauth2/v3/certs"

    def __init__(self, token: str, provider: Literal["google", "yahoo"]) -> None:
        self.token = token
        self.provider = provider

    def fetchCerts(self):
        """
        Gets all the public certs from google's api
        """

        if self.provider == "google":
            response = requests.get(self.PublicKeyUrl)
        else:
            raise TypeError(f"Only Provider Accessible is Google, got {self.provider} instead")
        keys = response.json()
        return keys

    @property
    def kid(self):
        """
        Gets the decoded 'kid' value from the token
        """

        # Get decoded header in token
        unverified_header: dict = jwt.get_unverified_header(self.token)
        if not unverified_header or 'kid' not in unverified_header:
            raise ValueError(
                "Unable to extract 'kid' from the token header.", jwt=self.token)
        kid = unverified_header['kid']
        return kid

    @property
    def publicKey(self):
        """
        Gets the matching public key from google's api
        """

        pub: str | None = None

        for k in self.fetchCerts()["keys"]:            
            if k['kid'] == self.kid:
                pub = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(k))
                break

        if not pub:
            raise ValueError(f"Public key for {self.kid} not found")

        return pub

    @property
    def isValid(self):
        """
        Checks if a token is valid
        """
        try:
            jwt.decode(self.token, self.publicKey, algorithms=["RS256"], audience=self.decoded.aud)
            return True
        except Exception:
            return False

    @property
    def header(self):
        return self.token.split(".")[0]
    
    @property
    def payload(self):
        return self.token.split(".")[1]
    
    @property
    def signature(self):
        return self.token.split(".")[2]

    @property
    def decoded(self) -> JWTPayload:
        """
        Gets the decoded payload
        """
        raw: bytes = base64.b64decode(self.payload + "==")
        js: dict = json.loads(raw)
        struct: JWTPayload = JWTPayload(**js)
        return struct
