from flask import redirect, Blueprint, render_template, url_for, session, jsonify
from flask_login import login_required, login_user, logout_user

from .models import User
from .spotify import Spotify

views = Blueprint("views", __name__)


@views.route("/is-logged-in")
def is_logged_in():
    return jsonify({"is_logged_in": session.get('user_id') is not None})


@views.route("/display-name")
def display_name():
    user_id = session.get('user_id')
    # retrieve user info from MongoDB using the user_id from the session
    user = User.get(user_id)

    return jsonify({"display_name": user.display_name})


@views.route("/timeline-data")
def timeline_data():
    user_id = session.get('user_id')
    # retrieve user info from MongoDB using the user_id from the session
    user = User.get(user_id)

    timeline_data = []
    for month in user.timeline_data.keys():
        timeline_data.append({
            "month": month,
            # change to use get_top_tracks() method
            "data": user.get_top_tracks(month)
        })

    return jsonify(timeline_data)


@views.route("/tracks/<month>", defaults={"length": -1})
@views.route("/tracks/<month>/<length>")
def top_tracks_date(month, length):
    # cast month and length to correct types
    month = str(month)
    length = int(length)

    user_id = session.get('user_id')
    # retrieve user info from MongoDB using the user_id from the session
    user = User.get(user_id)

    if month not in user.timeline_data.keys():
        return jsonify([])

    tracks = user.get_top_tracks(month, length)

    return jsonify(tracks)


@views.route("/user-data")
def user_data():
    user_id = session.get('user_id')
    # retrieve user info from MongoDB using the user_id from the session
    user_doc = User.get_user_document(user_id)

    if user_doc is None:
        return jsonify({})
    # remove _id since it is not JSON serializable and not needed
    user_doc.pop("_id", None)

    return jsonify(user_doc)


@views.route("/top-tracks-playlist/<month>", defaults={"length": -1})
@views.route("/top-tracks-playlist/<month>/<length>")
def top_tracks_playlist(month, length):
    # cast month and length to correct types
    month = str(month)
    length = int(length)

    user_id = session.get('user_id')
    # retrieve user info from MongoDB using the user_id from the session
    user = User.get(user_id)

    playlist_name = f"Your {month} top {length}"

    if length != -1:
        description = f"Your top {length} songs for {month}"
    else:
        description = f"Your top songs for {month}"

    playlist_id = user.create_top_tracks_playlist(
        month, length, playlist_name, description)

    return jsonify({"playlist_id": playlist_id})


@views.route("/monthview-data/<month>")
def monthview_data(month):
    # cast month to correct type
    month = str(month)

    user_id = session.get('user_id')
    # retrieve user info from MongoDB using the user_id from the session
    user = User.get(user_id)

    monthview_data = user.get_monthview_data(month)

    return jsonify(monthview_data)
