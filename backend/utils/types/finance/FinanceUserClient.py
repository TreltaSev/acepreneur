import re
from typing import List, Literal
from utils.types.finance import FinanceTypes
from utils.exception import HighLevelException
from utils.types.oauth2 import UserClient
from utils.types.finance.FinanceTypes import Finance

from utils.mongo import MongoClient


class FinanceUserClient(UserClient):
    """
    ## Inherits from :class:`utils.types.oauth2.UserClient`
    Finance data accessible userClient object

    ### Inherited Params
    :param provider: Provider, i.e. api used for sign in. Valid providers include
    "Google", "Microsoft", "Yahoo", and "FinalFinance"
    :type provider: Literal["Google", "Microsoft", "Yahoo", "FinalFinance"]
    :param string name: User Name, Full name, like "Trelta Sebastion"
    :param string email: User Email
    :param string profile: User pfp image
    :param string id: User identifier given by

    ### Finance Params
    """

    def __init__(self, *args, **kwargs):

        # Type Annotations
        self.finance: Finance

        super().__init__(*args, **kwargs)

        # Create Defaults
        self.__defaults()

    def __defaults(self):
        """
        Sets defaults for :class:`FinanceUserClient`
        """
        self.dict.setdefault("finance", Finance())

    def _update_array_element(
        self,
        action: str,
        query: str,
        value: any,
        array_filters: List[dict],
        check: Literal["modified", "matched"],
    ):
        """
        This one's a doosey, higher level update_one method, capable of doing everything needed so far.
        This method uses the :mongo:`MongoClient.users` Collection

        Parameters
        ----------
        `action : str`
            DB action for arrays, auto prefixed with "$", update action
        `query : str`
            DB Query
        `array_filters : List[str]`
            Array filters for the method
        `check : Literal["modified", "matched"]`
            What value will be checked? modified or matched of operation.

        ## Usage
        ```python
        _update_array_element(
            {"provider": user.provider, "id": user.id},
            "push",
            "finance.savings.$[account].automations", {
                "name": name,
                "type": type,
                "id": id
            },
            [{"account.id": accountId}],
            "modified"
        )
        ```
        """

        # Prepare the query and action parameters
        operation = MongoClient.users.update_one(
            {"provider": self.provider, "id": self.id},
            {f"${action}": {query: value}},
            array_filters=array_filters,
        )

        # Buffering the result
        _val = 0

        match check:

            # Only checks if the key was found in the database
            case "matched":
                _val = operation.matched_count

            # Checks if the value was updated in the database
            case "modified":
                _val = operation.modified_count

        if _val == 0:
            raise HighLevelException(
                "Operation Failed", name="Array Element Update", action=action
            )

        return operation
