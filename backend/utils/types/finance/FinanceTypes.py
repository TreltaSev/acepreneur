import re
from utils.types import Struct
from utils.types.finance import FinanceUserClient
from typing import List, Any
import datetime
import numbers


class TimeStamp(Struct):
    """
    Time stamp class holding creation data, such as the creation date, creator

    Parameters
    ----------
    `created : int`
        Unix timestamp that shard was created
    `creator: str`
        Creator of shard.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create Defaults
        self.__defaults()

    def __defaults(self):
        """
        Sets defaults for :class:`Stamp`
        """
        self.dict.setdefault("created", datetime.datetime.now().timestamp())
        self.dict.setdefault("creator", "server")

class StampCompatible(Struct):
    """
    History Object, contains information pertaining to a specific savings event

    Parameters
    ----------
    `stamp : TimeStamp`
        Timestamp Object
    """

    def __init__(self, *args, **kwargs):

        # Type Annotation
        self.stamp: TimeStamp

        super().__init__(*args, **kwargs)

        # Create Defaults
        self.__defaults()

    def __defaults(self):
        """
        Sets defaults for :class:`SavingsHistory`
        """
        self.dict.setdefault("stamp", TimeStamp())
        
    def convert_date(self, value: str | Any, none_on_fail: bool = False) -> int | Any:
        
        
        
        if not isinstance(value, str):
            return value
        
        if "(" in value:
            value = value[:value.index(" (")]
        
        
        try:
            date_object = datetime.datetime.strptime(value, "%a %b %d %Y %H:%M:%S %Z%z")
            # Convert
            unix_time = int(date_object.timestamp())
            return unix_time
        except Exception:
            if (none_on_fail):
                return None
            return datetime.datetime.now().timestamp()


class SavingsHistory(StampCompatible):
    """
    History Object, contains information pertaining to a specific savings event

    Parameters
    ----------
    `type : str`
        Type of transaction, for now, either "deposit" "withdrawal" or "allocation"
    `target : str | None`
        Target of history object
    `origin : str | None`
        Origin of history object
    `id : str`
        Specific identification of the shard
    `amount : numbers.Real`
    Amount of object, like $200.00, it would show up as 200.00
    `stamp : TimeStamp`
        Stamp Object

    """

    modifiable = ["amount", "target", "to", "date_unix"]

    def __init__(self, *args, **kwargs):

        # Type Annotation
        self.type: str
        self.to: str | None
        self.source: str | None
        self.id: str | None
        self.amount: numbers.Real
        self.description: str | None
        self.date_unix: int | None

        super().__init__(*args, **kwargs)

        # Create Defaults
        self.__defaults()
        
        # Format Date
        self.__handle_date()

    def __defaults(self):
        """
        Sets defaults for :class:`SavingsHistory`
        """
        self.dict.setdefault("type", "deposit")
        self.dict.setdefault("to", None)
        self.dict.setdefault("source", None)
        self.dict.setdefault("id", None)
        self.dict.setdefault("amount", 0)
        self.dict.setdefault("description", None)
        self.dict.setdefault("date_unix", None)
        
    def __handle_date(self):
        try:
            _buff = str(self.date_unix)
            _buff = _buff[:_buff.index(" (")]
            _buff = datetime.datetime.strptime(_buff, "%a %b %d %Y %H:%M:%S %Z%z")

            # Convert
            unix_time = int(_buff.timestamp())
            self.date_unix = unix_time
        except Exception:
            pass
        
class TransactionHistory(SavingsHistory):
    """
    Inherits from :class:`SavingsHistory`
    
    Has all the attributes of savings history but also has category
    """
    
    modifiable = ["amount", "category", "description", "date_unix"]
    
    def __init__(self, *args, **kwargs):
        
        # Type annotation
        self.category: str | None
        
        super().__init__(*args, **kwargs)


class LinkedHistory(Struct):
    """
    Link history, dict with one key, that references a history object

    Parameters
    ----------
    `link : str`
        Link id
    """

    def __init__(self, *args, **kwargs):

        # Type Annotation
        self.link: str

        super().__init__(*args, **kwargs)

        # Create Defaults
        self.__defaults()

    def __defaults(self):
        """
        Sets defaults for :class:`SavingsHistory`
        """
        self.dict.setdefault("link", "")


class Pocket(StampCompatible):
    """
    Pocket, fund object.

    Parameters
    ----------
    `name : str`
        Name of pocket, i.e. College Fund
    `color : str`
        Color of college fund in hex format, i.e. #fff or #ffffff
    `amount : numbers.Real`
        Amount in pocket, like 9992.33
    `icon : str | None`
        Icon of pocket, saved as a string for predefined icons
    `history : List[PocketHistory]`
        History of specific pocket, like withdrawals and allocations    
    `id : str`
        Specific identification of the Pocket
    `stamp : TimeStamp`
        Stamp Object

    """

    modifiable = ["name", "color", "icon"]

    def __init__(self, *args, **kwargs):
        # Type Annotation
        self.name: str
        self.color: str
        self.amount: numbers.Real
        self.icon: str | None
        self.history: List[PocketHistory]
        self.id: str | None

        self._allowed_keys = ["history"]

        super().__init__(*args, **kwargs)

        # Create Defaults
        self.__defaults()

    def __defaults(self):
        """
        Sets defaults for :class:`Pocket`
        """
        self.dict.setdefault("name", "")
        self.dict.setdefault("color", "#fff")
        self.dict.setdefault("amount", 0.00)
        self.dict.setdefault("icon", None)
        self.dict.setdefault("history", [])
        self.dict.setdefault("id", None)

    def push_link(self, user: FinanceUserClient, history: SavingsHistory, accountId: str):
        """
        Pushes a link object to pockets, this link object contains a link key which can be used to reference 
        history objects in the root object.

        Parameters
        ----------
        `user : FinanceUserClient`
            User finance object
        `history : SavingsHistory`
            history object which will be turned into a link
        `accountId : str`
            id of savings account            
        """
        user._update_array_element(
            "push",
            "finance.savings.$[account].pockets.$[pocket].history",
            LinkedHistory(link=history.id).unwrap,
            [{"account.id": accountId}, {"pocket.id": self.id}],
            "modified"
        )


class PocketHistory(LinkedHistory):
    """
    Pocket History object, contains information of a specific action of a pocket
    Just a link

    Parameters
    ----------
    `link : str`
        Id of link object

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Goal(StampCompatible):
    """
    Goal object type

    Parameters
    ----------
    `name : str`
        Name of pocket, i.e. College Fund
    `color : str`
        Color of college fund in hex format, i.e. #fff or #ffffff
    `amount : numbers.Real`
        Amount in goal, like 9992.33
    `goal: float`
        Goal amount, like 15000.00
    `icon : str | None`
        Icon of goal, saved as a string for predefined icons
    `history : List[GoalHistory]`
        History of specific pocket, like withdrawals and allocations    
    `id : str`
        Specific identification of the shard
    `stamp : TimeStamp`
        Stamp Object

    """

    modifiable = ["name", "color", "goal", "icon", "description"]

    def __init__(self, *args, **kwargs):
        # Type Annotation
        self.name: str
        self.description: str | None
        self.color: str
        self.amount: numbers.Real
        self.goal: numbers.Real
        self.icon: str | None
        self.history: List[GoalHistory]
        self.id: str | None

        self._allowed_keys = ["history"]

        super().__init__(*args, **kwargs)

        # Create Defaults
        self.__defaults()

    def __defaults(self):
        """
        Sets defaults for :class:`Pocket`
        """
        self.dict.setdefault("name", "")
        self.dict.setdefault("color", "#fff")
        self.dict.setdefault("amount", 0.00)
        self.dict.setdefault("goal", 0.00)
        self.dict.setdefault("icon", None)
        self.dict.setdefault("history", [])

    def push_link(self, user: FinanceUserClient, history: SavingsHistory, accountId: str):
        """
        Pushes a link object to pockets, this link object contains a link key which can be used to reference 
        history objects in the root object.

        Parameters
        ----------
        `user : FinanceUserClient`
            User finance object
        `history : SavingsHistory`
            history object which will be turned into a link
        `accountId : str`
            id of savings account            
        """
        
        user._update_array_element(
            "push",
            "finance.savings.$[account].goals.$[goal].history",
            LinkedHistory(link=history.id).unwrap,
            [{"account.id": accountId}, {"goal.id": self.id}],
            "modified"
        )
        
        


class GoalHistory(LinkedHistory):
    """
    Goal History object, contains information of a specific action of a goal
    Just a link

    Parameters
    ----------
    `link : str`
        Id of link object
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Automation(StampCompatible):
    """
    Automation object,
    TODO: Somewhat barren, update it as seen fit

    Parameters
    ----------
    `name : str`
        Name of automation
    `type : str`
        Type of automation
    `id : str`
        Specific identification of the shard
    """

    modifiable = ["name", "type"]

    def __init__(self, *args, **kwargs):
        # Type Annotation
        self.name: str
        self.type: str
        self.id: str | None

        super().__init__(*args, **kwargs)

        # Create Defaults
        self.__defaults()

    def __defaults(self):
        """
        Sets defaults for :class:`Automation`
        """
        self.dict.setdefault("name", "")
        self.dict.setdefault("type", "")
        self.dict.setdefault("id", None)


class Savings(Struct):
    """
    Savings object, containing all of the relevant information below.

    Parameters
    ----------
    `id : str | None`
        Id of savings object        
    `name : str | None`
        Name of account    
    `type : str | None`
        Type of savings object
    `history : List[SavingsHistory]`
        List of information pertaining to a specific savings events
    `pockets : List[Pocket]`
        List of pockets
    `goals : List[Goal]`
        List of goals
    `automations : List[Automation]`
        List of automations
    """

    def __init__(self, *args, **kwargs):
        # Type Annotation
        self.id: str | None
        self.type: str | None
        self.history: List[SavingsHistory]
        self.pockets: List[Pocket]
        self.goals: List[Goal]
        self.automations: List[Automation]

        self._allowed_keys = ["history", "pockets", "goals", "automations"]

        super().__init__(*args, **kwargs)

        # Create Defaults
        self.__defaults()

    def __defaults(self):
        """
        Sets defaults for :class:`Savings`
        """
        self.dict.setdefault("id", None)
        self.dict.setdefault("name", None)
        self.dict.setdefault("type", "general")
        self.dict.setdefault("history", [])
        self.dict.setdefault("pockets", [])
        self.dict.setdefault("goals", [])
        self.dict.setdefault("automations", [])

    def push_history(self, user: FinanceUserClient, history: SavingsHistory, links: List[Struct] = []):

        # Push to main
        user._update_array_element(
            "push",
            "finance.savings.$[account].history",
            history.unwrap,
            [{"account.id": self.id}],
            "modified"
        )

        # Push link to children
        for link_child in links:
            if (hasattr(link_child, "push_link")):
                _call = getattr(link_child, "push_link", None)
                _call(user, history, self.id)


class IncomeHistory(StampCompatible):
    """
    Income history, whenever a income has to be applied, this is the data that represents it
    
    Parameters
    ---------
    `amount : number`
        Amount of income applied
    `stamp : TimeStamp`
        Timestamp object
    """
    
    def __init__(self, *args, **kwargs):
        # Type Annotation
        self.amount: int
        self.stamp: TimeStamp
        
        super().__init__(*args, **kwargs)
        
        # Create defaults
        self.__defaults()
    
    def __defaults(self):
        """
        Sets defaults for :class:`IncomeHistory`
        """
        self.dict.setdefault("amount", 0)

class IncomeStream(StampCompatible):
    """
    Specifies a user's income stream
    
    Parameters
    ----------
    `id : str`
        Identification of income stream
    `name : str`
        Name of income stream, such as Freelance Writing
    `amount : int`
        Amount of the income stream.
    `frequency : int`
        Frequency, how often this income stream will be applied in seconds
    `frequency_label : str`
        Human readable label directly linked to frequency
    `start : int`
        Starting date of this income stream in unix time format
    `end : int | none`
        End date of this income stream in unix time format
    `description : str | none`
        Optional description of the income stream
    `history: IncomeHistory[]`
        Income appliance history
    """
    
    modifiable = ["name", "amount", "frequency", "end", "description"]
    
    def __init__(self, *args, **kwargs):
        # --- Type Annotation --- #
        self.id: str
        self.name: str
        self.amount: int
        self.frequency: int
        self.frequency_label: str
        self.start: int
        self.end: int
        self.description: str | None
        self.history: List[LinkedHistory]
        self.links: List[LinkedHistory]
        
        self._allowed_keys = ["history"]
        
        super().__init__(*args, **kwargs)
        
        self.__defaults();
        
        self.__handle_dates()
        
        self.__handle_frequency_label()
        
    def __defaults(self):
        """
        Set defaults for :class:`IncomeStream` 
        """
        self.dict.setdefault("name", "Income Stream")
        self.dict.setdefault("amount", 0)
        self.dict.setdefault("frequency", None)
        self.dict.setdefault("frequency_label", "monthly")
        self.dict.setdefault("start", datetime.datetime.now().timestamp())
        self.dict.setdefault("end", None)
        self.dict.setdefault("description", None)
        
    def __handle_dates(self):
        self.start = self.convert_date(self.start)
        self.end = self.convert_date(self.end, none_on_fail=True)
        
    def __handle_frequency_label(self):
        
        # Frequency already set, don't overwrite
        if self.frequency != None:
            return
        
        # Store timedelta args
        matches: dict = {
            "daily": {
                "days": 1
            }, 
            "weekly": {
                "weeks": 1
            },
            "bi-weekly": {
                "weeks": 2
            },
            "monthly": {
                "days": 30.44
            },
            "quarterly": {
                "days": 30.44*3
            },
            "yearly": {
                "days": 365.25
            }
        }
        
        self.frequency = datetime.timedelta(**matches.get(self.frequency_label, {"days": 10})).total_seconds()
        

class Transactions(Struct):
    """
    Transactions account object, containing all of the relevant information below.

    Parameters
    ----------
    `id : str | None`
        Id of savings object
    `name : str | None`
        Name of account    
    `description : str | None`
        General description of account, defined by user        
    `history : List[SavingsHistory]`
        List of information pertaining to a specific transaction events
    `income_streams : List[IncomeStream]`
        List of user income streams
    """

    def __init__(self, *args, **kwargs):
        # Type Annotation
        self.id: str | None
        self.name: str | None        
        self.history: List[TransactionHistory]
        self.income_streams: List[IncomeStream]
        
        self._allowed_keys = ["history", "income_streams"]


        super().__init__(*args, **kwargs)

        # Create Defaults
        self.__defaults()

    def __defaults(self):
        """
        Sets defaults for :class:`Automation`
        """
        self.dict.setdefault("id", None)
        self.dict.setdefault("name", None)
        self.dict.setdefault("history", [])
        self.dict.setdefault("income_streams", [])


class Finance(Struct):
    """
    Savings object, containing all of the relevant information below.

    Parameters
    ----------
    `savings : Savings`
        Saving object
    `transactions: Transactions`
        Transactions Object

    """

    def __init__(self, *args, **kwargs):
        # Type Annotation
        self.savings: List[Savings]
        self.transactions: List[Transactions]

        self._allowed_keys = ["savings", "transactions"]

        super().__init__(*args, **kwargs)

        # Create Defaults
        self.__defaults()

    def __defaults(self):
        """
        Sets defaults for :class:`Savings`
        """
        self.dict.setdefault("savings", [])
        self.dict.setdefault("transactions", [])

    def parse_location(self, location: str, accountId: str | None = None) -> None:
        """
        Takes in a location symbol such as $savings_account:hndiwhao8y023...
        and tries to find a relevant option to the location
        """

        # Isolate key and id
        _patt = r"\$(\w+):([a-f0-9]{32})"

        _match = re.match(_patt, location)

        if not _match:
            return location

        key, id = _match.groups()

        _types = {
            "savings": Savings,
            "goals": Goal,
            "pockets": Pocket
        }

        obj = self

        # Change obj one level
        if key in ["goals", "pockets"]:
            obj = self.find_element("savings", accountId, Savings)

        return obj.find_element(key, id, _types[key])
