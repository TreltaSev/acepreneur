from utils.package import cloakquart
from utils.types import Struct
from utils.json import getJson
from utils.req import getHeaders, getUser

# Database
from utils.mongo import MongoClient
from utils.types import User


blueprint = cloakquart.Blueprint("api:@admin", __name__)

@blueprint.route("/api/admin/is", methods=["GET"])
@getHeaders(["Bearer"], explicit=True)
@getUser()
async def admin_is_GET(user: User):
    """
    Checks if the request holder is a admin.
    """
    
    is_admin = user.get("admin", False)
    
    return {
        "state": is_admin
    }
    
    