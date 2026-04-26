from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# Get MongoDB URI from environment variables
MONGO_URI = os.getenv("MONGO_URI")

if MONGO_URI:
    client = MongoClient(MONGO_URI)
    db = client["brain_tumor_db"]
    reports_collection = db["reports"]
else:
    client = None
    db = None
    reports_collection = None
    print("Warning: MONGO_URI not found in environment variables")