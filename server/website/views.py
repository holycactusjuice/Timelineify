from flask import redirect, Blueprint, render_template, url_for, session, jsonify
from flask_login import login_required, login_user, logout_user

from .models import User
from .spotify import Spotify

views = Blueprint("views", __name__)


@views.route("/user-data")
def user_data():
    user_id = session.get('user_id')
    # retrieve user info from MongoDB using the user_id from the session
    user_doc = User.get_user_document(user_id)
    # remove _id since it is not JSON serializable and not needed
    user_doc.pop("_id", None)

    return jsonify(user_doc)


@views.route("/top-tracks-playlist/<month>/<length>")
def top_tracks_playlist(month, length):
    # cast month and length to correct types
    month = str(month)
    length = int(length)

    user_id = session.get('user_id')
    # retrieve user info from MongoDB using the user_id from the session
    user = User.get(user_id)

    playlist_name = f"Your {month} top {length}"
    description = f"Your top {length} songs for {month}"

    playlist_id = user.create_top_tracks_playlist(
        month, length, playlist_name, description)

    return jsonify({"playlist_id": playlist_id})


@views.route("/overview-data")
def overview_data():
    user_id = session.get('user_id')
    # retrieve user info from MongoDB using the user_id from the session
    user = User.get(user_id)

    overview_data = user.get_overview_data()

    return jsonify(overview_data)
