from utils.exception import HighLevelException
from utils.mongo import MongoClient
from utils.package import cloakquart
from utils.types import User, Struct, Event, Secret
import json

from ._tools import insertEvent

from utils.json import getJson

from utils.req import requireAdmin, getUser, getHeaders

blueprint = cloakquart.Blueprint("api:@event-admin", __name__)
eventAdmin = blueprint.refactor_route(
    "/api/event/admin/redeem/<_secret>", methods=["GET"])


@blueprint.route("/api/event/admin/generate", methods=["POST"])
@getHeaders(["Bearer"], explicit=True)
@getUser()
@requireAdmin()
@getJson
async def event_admin_generate_POST(json_struct: Struct, *args, **kwargs):
    """
    Generates a secret that can be redeemed to make a user an event admin. This secret is then returned.
    """
    # Assume Decorator Caught User Log in.
    json_struct.requires(["slug"])

    Search = MongoClient.events.find_one({"slug": json_struct.slug})

    # Check if event with slug event exists
    if not Search:
        raise HighLevelException(f"Failed to locate event with the slug: {json_struct.slug}")

    return {
        "secret": Secret.create(slug=json_struct.slug, type="event-admin").sanitized(),
    }


@eventAdmin.on("GET")
@getHeaders(["Bearer"], explicit=True)
@getUser()
async def event_admin_redeem_GET(user: User, _secret: str, *args, **kwargs):
    """
    Get a specific registered event;

    """
    # Assume Decorator Caught User Log in.
    Search = MongoClient.secrets.find_one({"secret": _secret})

    if not Search:
        raise HighLevelException(f"Failed to locate secret")

    secret = Secret(Search)

    print(json.dumps(secret.sanitized(), indent=4))

    if (secret.expired):
        secret.delete()

    EventSearch = MongoClient.events.find_one({"slug": secret.slug})

    if not EventSearch:
        raise HighLevelException(f"Failed to locate event")

    event = Event(EventSearch)

    MongoClient.events.update_one(
        {"slug": secret.slug},
        {"$addToSet": {"admins": user.id}}
    )
    was_added = user.id in MongoClient.events.find_one({"slug": secret.slug}).get("admins", [])

    return {
        "added": was_added,
        "event": event.sanitized()
    }
