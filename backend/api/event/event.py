from utils.package import cloakquart
from utils.json import getJson
from utils.req import requireAdmin, getUser, getHeaders

from utils.helper import requires
from utils.mongo import MongoClient
from utils.types import User

blueprint = cloakquart.Blueprint("api:@event", __name__)
eventRefactor = blueprint.refactor_route("/api/event", methods=["GET", "POST", "DELETE", "PATCH"])

@blueprint.route("/api/events", methods=["GET"])
@getHeaders(["Bearer"], explicit=True)
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
@getHeaders(["Bearer"], explicit=True)
@getUser()
async def event_GET(*args, **kwargs):
    
    # Get Event
    return ":)"

@eventRefactor.on("POST")
@getHeaders(["Bearer"], explicit=True)
@getUser()
@requireAdmin()
async def event_POST(user: User, *args, **kwargs):
    print(user.id)
    return {
        "hey": "there :)"
    }
    

@eventRefactor.on("DELETE")
@getHeaders(["Bearer"], explicit=True)
@getUser()
@requireAdmin()
async def event_DELETE(user: User, *args, **kwargs):
    return {
        "hey": "there :)"
    }
    
    
@eventRefactor.on("PATCH")
@getHeaders(["Bearer"], explicit=True)
@getUser()
@requireAdmin()
async def event_PATCH(user: User, *args, **kwargs):
    return {
        "hey": "there :)"
    }