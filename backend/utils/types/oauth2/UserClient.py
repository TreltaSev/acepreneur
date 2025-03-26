from utils.types import Struct
from typing import Literal

class UserClient(Struct):
    """
    Stores type-hinting information for user client such as name, email, provider, id, and profile.

    ## Usage
    ```python
    ClientData: dict = {"provider": "google", "name": "Trelta Sebastion", "email": "treltasev@gmail.com", "profile": "https://longling.png", "id": "8282109..."}
    UserData = UserClient(**ClientData)
    UserData.dict # Dict Representation
    ```

    
    :param provider: Provider, i.e. api used for sign in. Valid providers include
    "Google", "Microsoft", "Yahoo", and "FinalFinance"
    :type provider: Literal["Google", "Microsoft", "Yahoo", "FinalFinance"]
    :param string name: User Name, Full name, like "Trelta Sebastion"
    :param string email: User Email
    :param string profile: User pfp image
    :param string id: User identifier given by    
    """

    def __init__(self, *args, **kwargs):
        # Type Annotation
        self.provider: Literal["Google", "Microsoft", "Yahoo", "FinalFinance"]
        self.name: str
        self.email: str
        self.profile: str
        self.id: str

        # Pop _id object
        kwargs.pop("_id", None)
        
        super().__init__(*args, **kwargs)
        
        # Create Defeaults
        self.__defaults()
    
    def __defaults(self):
        """
        Sets defaults
        """
        from utils.types.finance.FinanceTypes import Finance
        self.dict.setdefault("finance", Finance().unwrap)

        