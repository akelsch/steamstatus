from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from configuration import DB_LOCATION, UPDATE_FREQUENCY

# Flask
app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////" + DB_LOCATION
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Database
db = SQLAlchemy(app)

# Scheduler
scheduler = BackgroundScheduler()

# Imports after app and db are initialized
import views
from utils import init_db, update_db


@app.before_first_request
def initialize_app():
    # Run an update once at app start and start the scheduler afterwards
    schedule_update()
    scheduler.start()


@scheduler.scheduled_job("interval", seconds=UPDATE_FREQUENCY)
def schedule_update():
    init_db()
    update_db()
