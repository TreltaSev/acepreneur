
from utils.package import cloakquart
from utils.types import Program
from utils.req import getHeaders, getUser
from utils.mongo import MongoClient
from utils.exception import HighLevelException

blueprint = cloakquart.Blueprint("api:@program", __name__)
programRefactor = blueprint.refactor_route("/api/program/<_id>", methods=["GET"])


@blueprint.route("/api/programs", methods=["GET"])
@getHeaders(["Bearer"], explicit=True)
@getUser()
async def program_GET(*_, **__):
    """
    Get all registered programs;

    Requirements:
    -------------
    - User needs to be signed in
    """

    programs = list(MongoClient.programs.find({}))

    return {
        "programs": [Program(program).sanitized() for program in programs]
    }


@programRefactor.on("GET")
@getHeaders(["Bearer"], explicit=True)
@getUser()
async def program_GET(_id: str, *_, **__):
    """
    Get a specific registered program;
    """
    # Assume Decorator Caught User Log in.
    Search = MongoClient.programs.find_one({"id": _id})

    if not Search:
        raise HighLevelException(f"Failed to locate program of id {_id}")

    program = Program(Search)

    return {
        "program": program,
    }
