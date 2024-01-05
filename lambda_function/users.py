from pymongo import MongoClient
import os

MONGODB_USERNAME = os.environ['MONGODB_USERNAME']
MONGODB_PASSWORD = os.environ['MONGODB_PASSWORD']
DB_NAME = os.environ['DB_NAME']

client = MongoClient(
    f'mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@cluster0.iruvwvi.mongodb.net/test?retryWrites=true&w=majority')
db = client[DB_NAME]
users = db['users']
