from utils.exception import HighLevelException
from utils.mongo import MongoClient
from utils.package import cloakquart
from utils.types import User, Struct, Event


from ._tools import insertEvent

from utils.json import getJson

from utils.req import requireAdmin, getUser, getHeaders

blueprint = cloakquart.Blueprint("api:@event", __name__)
eventRefactor = blueprint.refactor_route(
    "/api/event/<_id>", methods=["GET", "POST", "DELETE", "PATCH", "PUT"])


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

    events = list(MongoClient.events.find({}))

    # If not admin, sanitize results considerably
    if not user.get("admin", False):
        events = [Event(event).client_safe for event in events]
    else:
        events = [Event(event).sanitized() for event in events]

    return {
        "events": events
    }


@eventRefactor.on("GET")
@getHeaders(["Bearer"], explicit=True)
@getUser()
async def event_GET(user: User, _id: str, *args, **kwargs):
    """
    Get a specific registered event;

    """
    # Assume Decorator Caught User Log in.
    Search = MongoClient.events.find_one({"id": _id})

    if not Search:
        raise HighLevelException(f"Failed to locate event of id {_id}")

    event = Event(Search)
    as_admin: bool = user.get("admin", False) or (user.id in event.admins)
    
    # If not admin, sanitize results considerably
    if not user.get("admin", False):
        event = event.client_safe
    else:
        event = event.sanitized()

    
    
    print("as admin", as_admin)
    event.asAdmin = as_admin
    
    return {
        "event": event,
    }


@blueprint.route("/api/event", methods=["POST"], endpoint="root_post")
@getHeaders(["Bearer"], explicit=True)
@getUser()
@requireAdmin()
@getJson
async def event_POST(user: User, json_struct: Struct, *args, **kwargs):

    event_details: dict = json_struct.filtered([
        "name",
        "description",
        "card",
        "slug",
        "content",
        "announcement",
        "reactions"
    ])

    event: Event = Event(event_details)

    insertEvent(event)

    return event.sanitized()


@eventRefactor.on("DELETE")
@getHeaders(["Bearer"], explicit=True)
@getUser()
@requireAdmin()
async def event_DELETE(_id: str, *args, **kwargs):

    MongoClient.events.find_one_and_delete({"id": _id})

    return {
        "message": f"Deleted event of id: {_id}"
    }


@eventRefactor.on("PATCH")
@getHeaders(["Bearer"],  explicit=True)
@getUser()
@getJson
async def event_PATCH(json_struct: Struct, user: User, _id: str, *args, **kwargs):
    """
    So... here, I might do something stupid and just "trust" the user.

    Requirements
    ------------
    - User to be logged in
    - Admin of specified event  
    """

    json_struct.requires(["update"])

    Search = MongoClient.events.find_one({"id": _id})

    if not Search:
        raise HighLevelException(f"Failed to locate event of id {_id}")
    

    event = Event(Search)
    
    # Check if user is either a dev admin or a event admin
    if not (user.get("admin", False) or user.id in event.admins):
        raise HighLevelException("You are missing the required permissions to access this resource")

    event.update(json_struct.update)

    Result = MongoClient.events.replace_one({"id": _id}, event.unwrap)

    return Result.raw_result

@eventRefactor.on("PUT")
@getHeaders(["Bearer"],  explicit=True)
@getUser()
@requireAdmin()
@getJson
async def event_PUT(json_struct: Struct, _id: str, *args, **kwargs):
    """
    So... here, I might do something stupid and just "trust" the user.

    Requirements
    ------------
    - User to be logged in
    - Administrator Login    
    """

    json_struct.requires(["admin_id"])
    
    # Ensure event exists
    EventSearch = MongoClient.events.find_one({"id": _id})
    if not EventSearch:
        raise HighLevelException(f"Event with id \"{EventSearch}\" was not found.")

    # Ensure user exists
    UserSearch = MongoClient.users.find_one({"id": json_struct.admin_id})    
    if not UserSearch:
        raise HighLevelException(f"User with id \"{json_struct.admin_id}\" was not found.")
        
    # Update Document, specifically the admin array
    UpdateResult = MongoClient.events.update_one({"id": _id}, {"$addToSet": {"admins": json_struct.admin_id}})
    
    return UpdateResult.raw_result
