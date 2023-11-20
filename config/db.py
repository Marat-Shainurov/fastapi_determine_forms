import os

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv('.env')

client = MongoClient(os.getenv('DATABASE_CLIENT_ADDRESS_AND_PORT'), connect=False)
collection_name = os.getenv('COLLECTION_NAME')
db_name = os.getenv('DATABASE_NAME')

db = client.get_database(db_name)
forms_collection = db.get_collection(collection_name)
forms_collection.create_index('name', unique=True)

if collection_name not in db.list_collection_names():
    db.create_collection(collection_name)

client.server_info()
