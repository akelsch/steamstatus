import json
from collections import OrderedDict

from flask import render_template, jsonify

from app import app
from models import Status


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/status.json")
def status():
    latest_status = Status.query.order_by(Status.timestamp.desc()).first().json
    decoder = json.JSONDecoder(object_pairs_hook=OrderedDict)

    return jsonify(decoder.decode(latest_status))
