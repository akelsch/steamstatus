import os

from flask import Flask

from steamstatus.config import API_KEY


def create_app():
    app = Flask(__name__)

    DB_SCHEME = "sqlite:///" if os.name == "nt" else "sqlite:////"
    DB_URI = DB_SCHEME + os.path.join(app.instance_path, "steamstatus.sqlite")

    app.config.from_mapping(
        JSON_SORT_KEYS=False,
        SQLALCHEMY_DATABASE_URI=DB_URI,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SCHEDULER_TIMEZONE="Europe/Berlin"
    )

    # Ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # Ensure API key is set
    if not API_KEY:
        raise Exception("Missing Steam API key in config.py")

    # Initialize database
    from steamstatus import db
    db.init_app(app)

    # Initialize scheduler
    from steamstatus import scheduler
    scheduler.init_app(app)

    # Initialize views
    from steamstatus.view import bp
    app.register_blueprint(bp)

    return app
