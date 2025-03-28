import os
import pymongo
import pymongo.collection
import pymongo.database


class MongoClient:
    client: pymongo.MongoClient = pymongo.MongoClient(os.getenv("MONGO_URL") or "mongodb://localhost:27017/")
    database: pymongo.database.Database = client["eday"]
    
    # Collections
    logs: pymongo.collection.Collection = database["logs"]
    users: pymongo.collection.Collection = database["users"]
    events: pymongo.collection.Collection = database["events"]