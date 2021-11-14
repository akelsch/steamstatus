import os

import toml
from flask import Flask


def create_app():
    app = Flask(__name__)

    DB_SCHEME = "sqlite:///" if os.name == "nt" else "sqlite:////"
    DB_URI = DB_SCHEME + os.path.join(app.instance_path, "steamstatus.sqlite")

    app.config["API_KEY"] = os.environ.get("API_KEY")
    app.config.from_file("config.toml", load=toml.load)
    app.config.from_mapping(
        JSON_SORT_KEYS=False,
        SQLALCHEMY_DATABASE_URI=DB_URI,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SCHEDULER_TIMEZONE="Europe/Berlin"
    )

    # Ensure API key is set
    if not app.config.get("API_KEY"):
        raise ValueError("No Steam Web API Key provided")

    # Ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

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
