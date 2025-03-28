# Database
from utils.mongo import MongoClient
from utils.types.user import User

# Id Generation
import secrets


def insertUser(user: User) -> User:
    """
    Takes in a user object and inserts it into the database if it doesn't exist.
    If a user.id isn't specified, its created.
    
    :param user: User Object, should be generated before. This is what will be inserted
    :type user: utils.types.user.User
    
    :rtype: utils.types.user.User
    
    Collections Used:
    -----------------
    - `MongoClient.Users` For storing user data
    
    Example:
    --------
    ```python
    user: User = User({"name": "name-test"}) # Since no id is specified, its generated
    inserted_user = insertUser(user)
    
    >>> insert.id
    'user-bnd8wbadaw...'
    
    ```
    """
    
    # Check if user already exists
    Search = MongoClient.users.find_one({"id": user.id})
    
    if not Search:
        
        if (user.id == None):
            
            # No user id specified, create it
            user.id = f"user-{secrets.token_hex(16)}"
        
        # User doesn't exist in database, create it
        MongoClient.users.insert_one(user.dict)
        
    return user