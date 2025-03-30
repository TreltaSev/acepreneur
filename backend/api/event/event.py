from utils.exception import HighLevelException
from utils.mongo import MongoClient
from utils.package import cloakquart
from utils.types import User, Struct, Event


from ._tools import insertEvent

from utils.json import getJson

from utils.req import requireAdmin, getUser, getHeaders

blueprint = cloakquart.Blueprint("api:@event", __name__)
eventRefactor = blueprint.refactor_route(
    "/api/event/<_id>", methods=["GET", "POST", "DELETE", "PATCH"])


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

    # If not admin, sanitize results considerably
    if not user.get("admin", False):
        event = event.client_safe
    else:
        event = event.sanitized()

    return {
        "event": event
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
@getHeaders(["Bearer"], explicit=True)
@getUser()
@requireAdmin()
async def event_PATCH(_id, *args, **kwargs):
    return {
        "hey": "there :)"
    }
