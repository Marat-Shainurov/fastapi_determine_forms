import os

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv('.env')

client = MongoClient(os.getenv('CLIENT_ADDRESS_AND_PORT'), connect=False)

db = client.get_database("db_determine_forms")
forms_collection = db.get_collection("forms_collection")
forms_collection.create_index('name', unique=True)

if "forms_collection" not in db.list_collection_names():
    db.create_collection("forms_collection")

client.server_info()
