from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("MONGODB_URI")
if not uri:
    raise ValueError("Set MONGODB_URI in .env")

client = MongoClient(uri)
db = client[os.getenv("DATABASE_NAME", "todo_db")]
collection = db[os.getenv("COLLECTION_NAME", "todos")]