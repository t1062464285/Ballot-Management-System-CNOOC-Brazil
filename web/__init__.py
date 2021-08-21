import flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from werkzeug.security import generate_password_hash
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = flask.Flask(__name__)
    app.config['SECRET_KEY'] = 'abcabcabc'
    app.config['SQLALCHEMY_DATABASE_URI']=f"sqlite:///{DB_NAME}"
    db.init_app(app)

    # import every routes from routes.py
    from .routes import routes
    app.register_blueprint(routes, url_prefix='/')
    
    from .models import User

    create_db(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'routes.login'

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_db(app):
    if not path.exists("web/"+DB_NAME):
        db.create_all(app=app)
        print ("create database")
