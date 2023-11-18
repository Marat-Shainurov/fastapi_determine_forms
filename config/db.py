import os

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv('.env')

client = MongoClient(os.getenv('CLIENT_ADDRESS_AND_PORT'), connect=False)

db = client.get_database("db_determine_forms")
secrets_collection = db.get_collection("determine_forms")

if "determine_forms" not in db.list_collection_names():
    db.create_collection("determine_forms")

client.server_info()
