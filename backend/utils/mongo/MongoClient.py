import os
import json
import pymongo
import pymongo.collection
import pymongo.database
from pyucc import console
from siblink import Config
from utils.types import Struct

class MongoClient:
    print(os.getenv("MONGO_URL") or "mongodb://localhost:27017/")
    print(os.getenv("MONGO_URL"))
    print(json.dumps(Struct(Config.__dict__).sanitized(), indent=4))
    client: pymongo.MongoClient = pymongo.MongoClient(os.getenv("MONGO_URL") or "mongodb://localhost:27017/")
    database: pymongo.database.Database = client["eday"]

    # Collections
    logs: pymongo.collection.Collection = database["logs"]
    users: pymongo.collection.Collection = database["users"]
    events: pymongo.collection.Collection = database["events"]
    
    @classmethod
    def refresh_client(cls):
        
        # Refresh client and database
        cls.client = pymongo.MongoClient(os.getenv("MONGO_URL") or "mongodb://localhost:27017/")
        cls.database = cls.client["eday"]
        
        # Clear existing collections
        existing = set(cls.__dict__.keys())
        for attr in existing:
            if isinstance(getattr(cls, attr, None), pymongo.collection.Collection):
                delattr(cls, attr)
        
        # Dynamically Assign Collections
        for collection in cls.database.list_collection_names():
            setattr(cls, collection, cls.database[collection])

