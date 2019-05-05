import os

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from configuration import UPDATE_FREQUENCY

app = Flask(__name__)

db_scheme = "sqlite:///" if os.name == "nt" else "sqlite:////"
db_url = db_scheme + os.path.join(app.instance_path, "steamstatus.sqlite")
# Ensure the instance folder exists
os.makedirs(app.instance_path, exist_ok=True)

app.config.from_mapping(
    JSON_SORT_KEYS=False,
    SQLALCHEMY_DATABASE_URI=db_url,
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

db = SQLAlchemy(app)
scheduler = BackgroundScheduler()

import views
from db import init_db, update_db


@app.before_first_request
def init_app():
    # Initialize database
    init_db()
    update_db()

    # Start scheduler
    scheduler.add_job(update_db, "interval", seconds=UPDATE_FREQUENCY)
    scheduler.start()
