

from utils.package import cloakquart
from utils.types import Struct, User
from utils.json import getJson
from utils.req import getHeaders, getUser




blueprint = cloakquart.Blueprint("api:@admin", __name__)
adminRefactor = blueprint.refactor_route("/api/admin/is", methods=["GET", "POST"])

@adminRefactor.on("GET")
@getHeaders(["Bearer"], explicit=True)
@getUser()
async def admin_is_GET(user: User, *args, **kwargs):
    """
    Checks if the request holder is a admin.
    """
    
    print("Hi there :0")
    
    is_admin = user.get("admin", False)
    
    return {
        "state": is_admin
    }
    
# @adminRefactor.on("POST")
# @getJson
# async def admin_is_POST(json_struct: Struct, *args, **kwargs):
#     json_struct.requires(['secret'])
#     return {
#         "status": json_struct.secret == Config.admin.secret
#     }
    