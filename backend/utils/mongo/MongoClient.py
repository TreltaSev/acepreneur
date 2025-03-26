import os
import pymongo
import pymongo.collection
import pymongo.database


class MongoClient:
    client: pymongo.MongoClient = pymongo.MongoClient(os.getenv("MONGO_URL") or "mongodb://localhost:27017/")
    database: pymongo.database.Database = client["finalfinance"]
    
    # Collections
    logs: pymongo.collection.Collection = database["logs"]
    sessions: pymongo.collection.Collection = database["sessions"]
    users: pymongo.collection.Collection = database["users"]
    credentials: pymongo.collection.Collection = database["credentials"]