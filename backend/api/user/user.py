from utils.package import cloakquart
from utils.types import Struct
from utils.json import getJson
from utils.req import getHeaders, getUser

# Database
from utils.mongo import MongoClient
from utils.types import User

# Route specific tools
from ._tools import insertUser

blueprint = cloakquart.Blueprint("api:@user", __name__)
userCallback = blueprint.refactor_route(
    "/api/user", methods=["GET", "DELETE", "POST"])


@userCallback.on("POST")
@getHeaders(["Admin-Token"])
async def user_POST(headers: Struct, *args, **kwargs):
    user: User = User(headers=headers)
    user = insertUser(user)
    return user.sanitized()


@userCallback.on("GET")
@getHeaders(["Bearer"], explicit=True)
@getUser()
async def user_GET(headers: Struct, user: User, *args, **kwargs):
    # Respond with token
    return user.sanitized()
    


@userCallback.on("DELETE")
@getHeaders(["Bearer"], explicit=True)
async def user_DELETE(headers: Struct, *args, **kwargs):
    MongoClient.users.find_one_and_delete({"id": headers.Bearer})
    return {
        "message": f"Deleted session of token: {headers.Bearer}"
    }
