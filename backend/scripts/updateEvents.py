"""
From the mongo database, clears the events collection and 
injects the events template from /templates/events
"""
import re
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

# Refresh & Load Client
MongoClient.refresh_client()

# Create Events Collection if it doesn't exist
try:
    MongoClient.database.create_collection("events")
except CollectionInvalid as e:
    pass


# Clear Collection
MongoClient.events.delete_many({})

def set_nested(d, keys, value):
    for key in keys[:-1]:
        d = d.setdefault(key, {})
    d[keys[-1]] = value
    

_file = Path(Config.root / "../templates/event/[slug]").glob("*.svelte")

parsed = []

for file in list(_file):
    text = file.read_text()
    metadata_block = re.search(r"<!--@metadata(.*?)-->", text, re.DOTALL)
    content_html = re.sub(r"<!--@metadata.*?-->", "", text, flags=re.DOTALL).strip()
    metadata = {}

    for line in metadata_block.group(1).strip().splitlines():
        if not line.strip():
            continue
        key, val = line.split("=", 1)
        keys = key.strip().split(".")
        val = val.strip().strip('"')  # remove wrapping quotes
        set_nested(metadata, keys, val)
    
    _event = Event({**metadata, "content": {"blueprint": content_html}})
    if "id" not in metadata:
        _event.id = f"event-{_event.slug}"
        
    if "order" in metadata:
        _event.order = int(_event.order)
        
    parsed.append(_event)

console.done("Parsed all events")

MongoClient.events.insert_many([parse_object.unwrap for parse_object in parsed])

console.done("Wrote Events to Collection")
    