import secrets
from utils.types import Struct
from utils.mongo import MongoClient
from datetime import datetime, timedelta


class Secret(Struct):
    """
    Object used to store secret data for redeeming secrets, generating QR codes, etc.

    ## Usage
    ```python
    from utils.types.secret.secret import Secret

    # Example data
    data = {
        "secret": "user-idhjwa...",
        "qrUrl": "https://example.com/qr-code",
        "expiresAt": "2023-12-31 23:59:59.000000"
    }

    # Create a Secret object
    secret = Secret.create(data)

    # Access properties
    print(secret.secret)  # Output: user-idhjwa...
    print(secret.qrUrl)   # Output: https://example.com/qr-code
    print(secret.expiresAt)  # Output: 2023-12-31 23:59:59.000000

    # Access as dictionary
    print(secret.dict)  # Dictionary representation of the object
    ```

    :param str secret: Unique identifier for the secret.
    :param str qrUrl: URL for the QR code associated with the secret.
    :param str expiresAt: Expiration timestamp for the secret in the format "%Y-%m-%d %H:%M:%S.%f".
    """

    def __init__(self, obj=None, **kwargs):
        # __ Type Annotation __
        self.secret: str
        self.qrUrl: str
        self.expiresAt: str

        super().__init__(obj, **kwargs)

        # __ Create Defaults __
        self.__defaults()

    def __defaults(self):
        """
        Sets the defaults for this object.
        """
        self.dict.setdefault("secret", secrets.token_hex(64))
        self.dict.setdefault("qrUrl", None)
        self.dict.setdefault("expiresAt", (datetime.now() + timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S.%f"))

    @property
    def expiresAtDatetime(self):
        """
        Converts the `expiresAt` string to a `datetime` object.
        """
        return datetime.strptime(self.expiresAt, "%Y-%m-%d %H:%M:%S.%f")

    def isExpired(self):
        """
        Checks if the secret is expired based on the current time.
        """
        return datetime.now() > self.expiresAtDatetime

    def delete(self):
        """
        Deletes the secret from the database.
        """
        MongoClient.secrets.find_one_and_delete({"secret": self.secret})

    @classmethod
    def create(cls, data=None, **kwargs):
        """
        Creates and stores a new Secret instance in the database.
        :param dict data: Optional dictionary with secret data.
        :param kwargs: Additional arguments for the secret.
        :return: A new Secret instance.
        """

        data = data or {}
        secret = cls(data, **kwargs)

        MongoClient.secrets.insert_one(secret.unwrap)
        return secret
