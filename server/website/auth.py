from flask import Flask, redirect, url_for, Blueprint

from .spotify import Spotify


auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return Spotify.spotify_login()


@auth.route("/callback")
def callback():
    Spotify.spotify_callback()
    return redirect(url_for("views.home"))
