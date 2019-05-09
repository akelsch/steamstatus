import os

import click
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

from steamstatus.config import API_KEY

app = Flask(__name__)

db_scheme = "sqlite:///" if os.name == "nt" else "sqlite:////"
db_uri = db_scheme + os.path.join(app.instance_path, "steamstatus.sqlite")
# Ensure the instance folder exists
os.makedirs(app.instance_path, exist_ok=True)

app.config.from_mapping(
    JSON_SORT_KEYS=False,
    SQLALCHEMY_DATABASE_URI=db_uri,
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

# Ensure API key is set
if not API_KEY:
    raise Exception("Missing Steam API key in config.py")

db = SQLAlchemy(app)
scheduler = BackgroundScheduler()

import steamstatus.core.views  # isort:skip


def init_db():
    db.drop_all()
    db.create_all()


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


app.cli.add_command(init_db_command)
