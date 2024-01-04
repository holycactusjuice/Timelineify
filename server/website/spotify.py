import base64
from datetime import datetime
from flask import redirect, session, request
from requests_oauthlib import OAuth2Session


class Spotify:
    client_id = "88405b10e1704946976efdef33e73f64"
    client_secret = "9f5d2959d24e461a9b64b7a38291c0cf"
    redirect_uri = "http://localhost:5000/callback"
    scope = ["playlist-modify-public", "playlist-modify-private",
             "ugc-image-upload", "user-read-recently-played", "user-read-private", "user-read-email",]
    auth_base_url = "https://accounts.spotify.com/authorize"
    token_url = "https://accounts.spotify.com/api/token"
    client_creds = f"{client_id}:{client_secret}"
    client_creds_b64 = base64.b64encode(client_creds.encode()).decode()
    response_type = "code"
    scopes = ["playlist-modify-public", "playlist-modify-private",
              "ugc-image-upload", "user-read-recently-played", "user-read-private", "user-read-email",]

    get_user_endpoint = "https://api.spotify.com/v1/me"
    create_playlist_endpoint = "https://api.spotify.com/v1/me/playlists"
    get_recently_played_endpoint = "https://api.spotify.com/v1/me/player/recently-played"

    # may change to static
    @classmethod
    def spotify_login(cls):
        # create OAuth2Session object with client_id, redirect_uri, and scope
        oauth = OAuth2Session(
            cls.client_id, redirect_uri=cls.redirect_uri, scope=cls.scopes)

        # create auth url and state from OAuth2Session object
        auth_url, state = oauth.authorization_url(Spotify.auth_base_url)

        # store state in session
        session['oauth_state'] = state

        return redirect(auth_url)

    @classmethod
    def spotify_callback(cls):
        oauth = OAuth2Session(
            cls.client_id, redirect_uri=cls.redirect_uri, state=session['oauth_state'])

        oauth.fetch_token(
            cls.token_url, authorization_response=request.url, client_secret=cls.client_secret)

        session['oauth_token'] = oauth.token

        return

    def to_unix(played_at):
        """converts played_at field given by Spotify API to unix timestamp in ms

        Args:
            played_at (str): played_at field given by Spotify API

        Returns:
            int: unix timestamp in ms
        """

        try:
            time = int(datetime.strptime(
                played_at, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp())
        except:
            time = int(datetime.strptime(
                played_at, "%Y-%m-%dT%H:%M:%SZ").timestamp())

        return time

    def unix_to_month(unix):
        """converts unix timestamp to month in format MM-YYYY

        Args:
            unix (int): unix timestamp

        Returns:
            str: MM-YYYY
        """

        return datetime.fromtimestamp(unix).strftime("%m-%Y")
