from pymongo import MongoClient
from config import Config

client = MongoClient(Config.mongodb+srv://Cih2026:Cih2026@cluster0.wzcir6b.mongodb.net/)
db = client["brain_tumor_db"]

reports_collection = db["reports"]