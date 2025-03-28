import quart

from utils.types.finance import FinanceUserClient
from utils.types.oauth2 import UserClient
from utils.package import cloakquart
from utils.types import Struct
from utils.json import getJson
from utils.req import getHeaders, getUser

from utils.helper import requires
from utils.helper.Router import router

blueprint = cloakquart.Blueprint("api:@program", __name__)
eventRefactor = blueprint.refactor_route("/api/program", methods=["GET", "POST", "DELETE", "PATCH"])

@eventRefactor.on("GET")
@getHeaders(["Bearer"], explicit=True)
async def program_GET(*args, **kwargs):
    return ":)"