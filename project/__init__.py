import os

from flask import Flask
from flask_login import LoginManager
from .commands import create_tables
from .extensions import db

def create_app():
    app = Flask(__name__)
    # Flask "secret keys" are random strings used to encrypt sensitive user data, such as passwords.
    app.config['SECRET_KEY'] = os.environ.get('OAUTH_SERVER_SECRET_KEY')
    database_url = os.environ.get('OAUTH_SERVER_DB_URL')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url.replace("postgres:", "postgresql:")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # register command to create tables in postgresql
    app.cli.add_command(create_tables)

    return app