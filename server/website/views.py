from flask import redirect, Blueprint, render_template, url_for, session
from flask_login import current_user, login_required, login_user, logout_user
from datetime import datetime

views = Blueprint("views", __name__)


@views.route("/")
def index():
    return "welcome to the index page"