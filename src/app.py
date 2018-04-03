import json
import os
import threading
from collections import OrderedDict
from datetime import datetime

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

from helpers import create_json

# Flask configuration
app = Flask("steamstatus")
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////" + os.path.join(basedir, "app.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JSON_SORT_KEYS"] = False
db = SQLAlchemy(app)

# App constants
APIKEY = "XXX"
TABLENAME = "status"


class Status(db.Model):
    """
    Database layout for storing statuses
    """
    __tablename__ = TABLENAME

    timestamp = db.Column(db.DateTime, primary_key=True)
    json = db.Column(db.Text, nullable=False)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/status.json", methods=["GET"])
def status_route():
    """
    URL route which serves the latest database entry as JSON
    """
    last_status = Status.query.order_by(Status.timestamp.desc()).limit(1).first()
    decoder = json.JSONDecoder(object_pairs_hook=OrderedDict)

    return jsonify(decoder.decode(last_status.json))


@app.before_first_request
def create_table():
    """
    Function to create the status table
    This is useful when running the app for the first time
    """
    if not db.engine.dialect.has_table(db.engine, TABLENAME):
        db.create_all()


@app.before_first_request
def update_database():
    """
    Function to update the database every 60 seconds
    """
    new_status = Status(timestamp=datetime.utcnow(), json=json.dumps(create_json(APIKEY)))
    db.session.add(new_status)
    db.session.commit()

    threading.Timer(60, update_database).start()
