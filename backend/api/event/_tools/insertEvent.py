# Database
from utils.mongo import MongoClient
from utils.types import Event

def insertEvent(event: Event) -> Event:
    """
    Takes in a event object and inserts it into the database if it doesn't exist.

    :param event: Event Object, should be generated before. This is what will be inserted
    :type user: utils.types.Event

    :rtype: utils.types.Event

    Collections Used:
    -----------------
    - `MongoClient.Events` For storing event data

    Example:
    --------
    ```python
    event: Event = Event({"name": "name-test"}) # Since no id is specified, its generated
    insertEvent(event)

    >>> event.present
    True

    ```
    """

    # Check if user already exists
    Search = MongoClient.users.find_one({"id": event.id})

    if not Search:
        # User doesn't exist in database, create it
        MongoClient.events.insert_one(event.unwrap)

    return event
