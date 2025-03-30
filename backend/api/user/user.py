import json
import traceback
from utils.types.oauth2 import UserClient
from utils.exception import HighLevelException
from utils.package import cloakquart
from utils.types import Struct
from utils.helper import requires
from utils.json import getJson
from utils.req import getHeaders, getUser

# Token Generation
import secrets

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
@getJson
async def user_POST(json_struct: Struct, headers: Struct, *args, **kwargs):
    json_struct.requires(["name"])
    name: str = json_struct.dict.pop("name")
    user: User = User(name=name, headers=headers)
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
