from flask import redirect, Blueprint, render_template, url_for, session
from flask_login import login_required, login_user, logout_user

from .models import User

views = Blueprint("views", __name__)


@views.route("/")
def index():
    return f"user_id: {session.get('user_id')}"


@views.route("/user-data")
def user_data():
    user_id = session.get('user_id')
    # retrieve user info from MongoDB using the user_id from the session
    user_doc = User.get_user_document(user_id)
    # remove _id since it is not JSON serializable and not needed
    user_doc.pop("_id", None)

    return user_doc
