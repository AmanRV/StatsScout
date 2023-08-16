from flask import Flask
from dotenv import load_dotenv
import os

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('FLASK_KEY')

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    return app