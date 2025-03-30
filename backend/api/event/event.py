from utils.package import cloakquart
from utils.json import getJson
from utils.req import getHeaders, getUser

from utils.helper import requires
from utils.mongo import MongoClient
from utils.types import User

blueprint = cloakquart.Blueprint("api:@event", __name__)
eventRefactor = blueprint.refactor_route("/api/event", methods=["GET", "POST", "DELETE", "PATCH"])

@blueprint.route("/api/events", methods=["GET"])
@getUser()
async def events_GET(user: User, *args, **kwargs):
    """
    Get all registered events;
    
    Requirements:
    -------------
    - User needs to be signed in
    """
    # Assume Decorator Caught User Log in.
    
    events = MongoClient.events.find({})
    print(events)
    
    return {
        "events": []
    }
    

@eventRefactor.on("GET")
@getUser()
async def event_GET(*args, **kwargs):
    
    # Get Event
    return ":)"