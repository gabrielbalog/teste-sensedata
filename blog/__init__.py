import os

from flask import Flask


def create_app(test_config=None):
    # Imports
    from . import db
    from blog import views

    # Creating APP
    app = Flask(__name__, instance_relative_config=True)

    # Configuring APP
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY"),
        SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Configure db
    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(views.bp)

    # Register Endpoints
    app.add_url_rule("/", endpoint="index")

    return app
