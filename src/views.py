from flask import jsonify, render_template

from app import app, db, scheduler
from config import UPDATE_FREQUENCY
from core import create_json
from models import Status


def update_status():
    new_status = Status(data=create_json())
    db.session.add(new_status)
    db.session.commit()


@app.before_first_request
def init():
    # Update once & start scheduler
    update_status()
    scheduler.add_job(update_status, "interval", seconds=UPDATE_FREQUENCY)
    scheduler.start()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/status.json")
def status():
    latest_status = Status.query.order_by(Status.id.desc()).first()
    return jsonify(latest_status.data)
