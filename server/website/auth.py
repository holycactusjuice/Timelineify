from flask import redirect, Blueprint, session, request, flash
from flask_login import login_required, login_user, logout_user
import requests
from urllib.parse import urlencode

from .spotify import Spotify
from . import users
from .models import User


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    auth_params = {
        'response_type': 'code',
        'client_id': Spotify.client_id,
        'scope': Spotify.scope,
        'redirect_uri': Spotify.redirect_uri,
        'state': Spotify.build_state()
    }
    auth_url = Spotify.auth_base_url + '?' + urlencode(auth_params)

    return redirect(auth_url)


@auth.route("/callback", methods=['GET', 'POST'])
def callback():
    auth_token = request.args['code']
    params = {
        'grant_type': 'authorization_code',
        'code': str(auth_token),
        'redirect_uri': Spotify.redirect_uri
    }
    headers = {
        'Authorization': f'Basic {Spotify.client_creds_b64}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(Spotify.token_url, params=params, headers=headers)

    session.permanent = True

    # if login is successful
    if response.status_code in range(200, 299):
        response_data = response.json()

        # get tokens from json
        access_token = response_data['access_token']
        refresh_token = response_data['refresh_token']

        # stores tokens in session
        session['access_token'] = access_token
        session['refresh_token'] = refresh_token

        # try to get user info from db
        user_info = User.get_account_info(access_token)
        user_id = user_info['id']
        user_doc = users.find_one({"user_id": user_id})

        # if the user is not in the db, add them
        if not user_doc:
            email = user_info['email']
            display_name = user_info['display_name']
            pfp_url = user_info['images'][0]['url']

            user = User(user_id, email, display_name,
                        pfp_url, access_token, refresh_token)

            users.insert_one(user.to_dict())
        # if the user is in the db, update their tokens
        else:
            user = User.get(user_id)
            user.access_token = access_token
            user.refresh_token = refresh_token

            user.update()

        login_user(user)
        session['user_id'] = user.user_id
    else:
        session['user_id'] = None

    session.modified = True

    # regardless of login success, redirect to home page
    return redirect("http://localhost:3000/")


@auth.route("/logout")
def logout():
    session['user_id'] = None
    # add spotify logout
    return redirect("https://accounts.spotify.com/en/logout")
