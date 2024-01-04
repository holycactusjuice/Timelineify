from models import Track, User
from . import users

for user_doc in users:
    user_id = user_doc["user_id"]
    access_token = user_doc["access_token"]
    User.update_timeline_data(user_id, access_token)
