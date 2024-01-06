from flask import Flask
from flask_login import LoginManager
from pymongo import MongoClient
from flask_pymongo import PyMongo
from flask_cors import CORS
import os
from dotenv import load_dotenv


load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
MONGODB_KEY = os.getenv('MONGODB_KEY')
MONGODB_USERNAME = os.getenv('MONGODB_USERNAME')
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')


client = MongoClient(
    f'mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@cluster0.iruvwvi.mongodb.net/{DB_NAME}?retryWrites=true&w=majority')
db = client[DB_NAME]
users = db['users']
tracks = db['tracks']


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.urandom(32)

    app.config['MONGO_URI'] = f'mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@cluster0.iruvwvi.mongodb.net/{DB_NAME}?retryWrites=true&w=majority'

    mongo = PyMongo()
    mongo.init_app(app)

    CORS(app, resources={
         r"/api/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    return app
