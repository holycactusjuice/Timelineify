from models import User
from users import users


def update_users_timeline_data():
    for user_doc in users.find():
        user = User.from_document(user_doc)
        user.update_timeline_data()
