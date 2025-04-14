"""
From the mongo database, clears the programs collection and 
injects the programs template from /templates/programs
"""
import re
import os
import json
from pathlib import Path
from pyucc import console
from siblink import Config
from dotenv import dotenv_values
from utils.mongo import MongoClient
from utils.types.program import Program
from pymongo.errors import CollectionInvalid

console.start("Injecting Programs")

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

# Create Programs Collection if it doesn't exist
try:
    MongoClient.database.create_collection("programs")
except CollectionInvalid as e:
    pass


# Clear Collection
MongoClient.programs.delete_many({})

def set_nested(d, keys, value):
    for key in keys[:-1]:
        d = d.setdefault(key, {})
    d[keys[-1]] = value
    

_file = Path(Config.root / "../templates/program/[slug]").glob("*.svelte")

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
    
    _program = Program({**metadata, "content": {"blueprint": content_html}})
    if "id" not in metadata:
        _program.id = f"program-{_program.slug}"
        
    if "order" in metadata:
        _program.order = int(_program.order)
        
    if "events" in metadata:
        _program.events = metadata["events"].split(";")
        
    parsed.append(_program)

console.done("Parsed all programs")

MongoClient.programs.insert_many([parse_object.unwrap for parse_object in parsed])

console.done("Wrote Programs to Collection")
