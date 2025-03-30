from utils.mongo import MongoClient
from utils.types import Struct
from typing import List
import datetime
import secrets


class EventReactions(Struct):
    """
    Object to store an event's reaction data

    :param likes: List of all the user(s) who've liked the event
    :type likes: List[str]
    """

    def __init__(self, obj=None, **kwargs):
        # __ Type Annotation __
        self.likes: List[str] | int

        super().__init__(obj, **kwargs)

        # __ Create Defaults __
        self.__defaults()

    def __defaults(self):
        """
        Sets the defaults for this object
        """
        self.dict.setdefault("likes", [])


class EventAnnouncement(Struct):
    """
    Object to store an event's announcement data

    :param str text: Announcement Text
    :param str author: Last person who modified the announcement
    :param int time: unix timestamp
    """

    def __init__(self, obj=None, **kwargs):
        # __ Type Annotation __
        self.text: str
        self.author: str
        self.time: int

        super().__init__(obj, **kwargs)

        # __ Create Defaults __
        self.__defaults()

    def __defaults(self):
        """
        Sets the defaults for this object
        """
        self.dict.setdefault("text", "")
        self.dict.setdefault("author", "server")
        self.dict.setdefault("time", datetime.datetime.now().timestamp())


class EventContent(Struct):
    """
    Object to store an event's content data

    :param str blueprint: Content html
    """

    def __init__(self, obj=None, **kwargs):
        # __ Type Annotation __
        self.blueprint: str

        super().__init__(obj, **kwargs)

        # __ Create Defaults __
        self.__defaults()

    def __defaults(self):
        """
        Sets the defaults for this object
        """
        self.dict.setdefault("blueprint", "<span>No Content</span>")


class EventCardImage(Struct):
    """
    Object to store an event's card image data

    :param str url: Url of the image for the card
    :param str _class: Extra CSS classes of the card image
    :param str style: Inline styling for the image of the card
    """

    def __init__(self, obj=None, **kwargs):
        # __ Type Annotation __
        self.url: str
        self._class: str
        self.style: str

        super().__init__(obj, **kwargs)

        # __ Create Defaults __
        self.__defaults()

    def __defaults(self):
        """
        Sets the defaults for this object
        """
        self.dict.setdefault("url", "")
        self.dict.setdefault("_class", "")
        self.dict.setdefault("style", "")


class EventCard(Struct):
    """
    Object to store an event's card data

    :param str color: Color or accent of the card

    :param image: Image data for the card
    :type image: EventCardImage
    """

    def __init__(self, obj=None, **kwargs):
        # __ Type Annotation __
        self.color: str
        self.image: EventCardImage

        super().__init__(obj, **kwargs)

        # __ Create Defaults __
        self.__defaults()

    def __defaults(self):
        """
        Sets the defaults for this object
        """
        self.dict.setdefault("color", "#000000")
        self.dict.setdefault("image", EventCardImage())


class Event(Struct):
    """
    Object to store event data

    :param str id: Identification of the event
    
    :param str name: Name of the event

    :param str description: Description of the event

    :param card: Card Banner Data
    :type card: EventCard

    :param str slug: Slug Route

    :param content: Render Content
    :type content: EventContent

    :param announcement: Event announcement data
    :type announcement: EventAnnouncement

    :param reactions: Event Reaction Data
    :type reactions: EventReactions    
    """

    def __init__(self, obj=None, **kwargs):
        # __ Type Annotation __
        self.name: str
        self.description: str
        self.card: EventCard
        self.slug: str
        self.content: EventContent
        self.announcement: EventAnnouncement
        self.reactions: EventReactions

        super().__init__(obj, **kwargs)

        # __ Create Defaults __
        self.__defaults()

    def __defaults(self):
        """
        Sets the defaults for this object
        """
        self.dict.setdefault("id", f"event-{secrets.token_hex(16)}")
        self.dict.setdefault("name", "Event Name")
        self.dict.setdefault("description", "Event Description")
        self.dict.setdefault("card", EventCard())
        self.dict.setdefault("slug", self.id)
        self.dict.setdefault("content", EventContent())
        self.dict.setdefault("announcement", EventAnnouncement())
        self.dict.setdefault("reactions", EventReactions())

    @property
    def present(self) -> bool:
        """
        Checks if the event is present within the database
        
        :rtype: bool
        """
        return bool(MongoClient.events.find_one({"id": self.id}))
    
    @property
    def client_safe(self) -> dict:
        """
        Returns a client-safe dict so that we don't get any security concerns
        """
        _dict = dict(self.sanitized()) # Copy
        del _dict["announcement"]["author"]
        _dict["reactions"]["likes"] = len(_dict["reactions"]["likes"])        
        return _dict