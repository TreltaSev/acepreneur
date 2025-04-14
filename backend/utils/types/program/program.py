from utils.mongo import MongoClient
from utils.types import Struct
from typing import List
import datetime
import secrets

from utils.types.event.event import EventCard, EventContent, EventCardImage

class ProgramCardImage(EventCardImage):
    """
    Object to store a program's card image data.

    Inherits from EventCardImage.
    """
    def __init__(self, obj=None, **kwargs):
        super().__init__(obj, **kwargs)
        

class ProgramContent(EventContent):
    """
    Object to store a program's content data.

    Inherits from EventContent.

    :param str blueprint: Content HTML
    """
    def __init__(self, obj=None, **kwargs):
        super().__init__(obj, **kwargs)


class ProgramCard(EventCard):
    """
    Object to store a program's card data.

    Inherits from EventCard.

    :param str color: Color or accent of the card
    :param image: Image data for the card
    :type image: EventCardImage
    """
    def __init__(self, obj=None, **kwargs):
        super().__init__(obj, **kwargs)

class Program(Struct):
    """
    Object to store program data.

    :param str id: Identification of the program
    :param str name: Name of the program
    :param str description: Description of the program
    :param card: Card banner data
    :type card: ProgramCard
    :param str slug: Slug route
    :param content: Render content
    :type content: ProgramContent
    """
    def __init__(self, obj=None, **kwargs):
        # __ Type Annotation __
        self.id: str
        self.name: str
        self.description: str
        self.card: ProgramCard
        self.slug: str
        self.content: ProgramContent

        super().__init__(obj, **kwargs)

    
        # __ Create Defaults __
        self.__defaults()

    def __defaults(self):
        """
        Sets the defaults for this object.
        """
        self.dict.setdefault("id", f"program-{secrets.token_hex(16)}")
        self.dict.setdefault("name", "Program Name")
        self.dict.setdefault("description", "Program Description")
        self.dict.setdefault("card", ProgramCard())
        self.dict.setdefault("slug", self.id)
        self.dict.setdefault("content", ProgramContent())