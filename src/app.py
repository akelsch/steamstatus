import json
import os
from collections import OrderedDict
from datetime import datetime

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

from helpers import create_json

# Flask configuration
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JSON_SORT_KEYS"] = False
db = SQLAlchemy(app)

# INSERT STEAM WEB API KEY HERE
apikey = "XXX"


# Database layout for storing statuses
class Status(db.Model):
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


def update_database():
    """
    Function to update the database every 60 seconds
    """

    #threading.Timer(60, update_database).start()

    new_status = Status(timestamp=datetime.utcnow(), json=json.dumps(create_json(apikey)))
    db.session.add(new_status)
    db.session.commit()


# Start the status update loop
update_database()
