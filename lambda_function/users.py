from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_USERNAME = os.getenv('MONGODB_USERNAME')
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

client = MongoClient(
    f'mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@cluster0.iruvwvi.mongodb.net/test?retryWrites=true&w=majority')
db = client[DB_NAME]
users = db['users']
