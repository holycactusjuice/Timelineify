from flask import redirect, Blueprint, session, request, url_for
import requests
from urllib.parse import urlencode

from .spotify import Spotify
from . import users
from .models import User


auth = Blueprint("auth", __name__)

@auth.route("/login")
def login():
    auth_params = {
        'response_type': 'code',
        'client_id': Spotify.client_id,
        'scope': Spotify.scope,
        'redirect_uri': Spotify.redirect_uri,
        'state': Spotify.build_state()
    }
    auth_url = Spotify.auth_base_url + '?' + urlencode(auth_params)

    # oauth 2.0 requires https redirect uri

    # # create OAuth2Session object with client_id, redirect_uri, and scope
    # oauth = OAuth2Session(
    #     cls.client_id, redirect_uri=cls.redirect_uri, scope=cls.scopes)

    # # create auth url and state from OAuth2Session object
    # auth_url, state = oauth.authorization_url(Spotify.auth_base_url)

    # # store state in session
    # session['oauth_state'] = state

    return redirect(auth_url)


@auth.route("/callback")
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
            user = User.from_user_id(user_id)
            user.access_token = access_token
            user.refresh_token = refresh_token

            user.update()

        print(user.to_json())

        return user.to_json()

    else:
        return "error"

    # oauth 2.0 requires https redirect uri

    # oauth = OAuth2Session(
    #     cls.client_id, redirect_uri=cls.redirect_uri, state=session['oauth_state'])

    # oauth.fetch_token(
    #     cls.token_url, authorization_response=request.url, client_secret=cls.client_secret)

    # session['oauth_token'] = oauth.token

    # return