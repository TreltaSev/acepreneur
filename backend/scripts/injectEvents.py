"""
From the mongo database, clears the events collection and 
injects the events template from /templates/events
"""

import os
import json
from pathlib import Path
from pyucc import console
from siblink import Config
from dotenv import dotenv_values
from utils.mongo import MongoClient
from utils.types.event import Event
from pymongo.errors import CollectionInvalid

console.start("Injecting Events")

# Load Customized Environment


@Config.load_predetermined
def _load_env():    
    project_root: Path = Path(Config.root / '../')
    Config.env = {
        **dotenv_values(project_root / ".env"),
        **dotenv_values(project_root / ".env.production.local")
    }
    os.environ.update(Config.env)  # Make sure os.gen_env works well


_load_env()

# Create Events Collection if it doesn't exist
try:
    MongoClient.database.create_collection("events")
except CollectionInvalid as e:
    pass

# Refresh & Load Client
MongoClient.refresh_client()
# Clear Collection



MongoClient.events.delete_many({})

console.done("Cleared Events Collection")

# Load Events Template
pTemplatesDirectory = Path(Config.root / "../templates/")
pEventsTemplate = pTemplatesDirectory / "events-template.json"

# Parse events template
events = [Event(event).unwrap for event in json.loads(pEventsTemplate.read_text())]

console.done("Parsed Events Template")

# Insert all events
MongoClient.events.insert_many(events)

console.done("Wrote Events to Collection")
