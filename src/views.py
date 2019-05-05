import json
from collections import OrderedDict

from flask import jsonify, render_template

from app import app
from models import Status


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/status.json")
def status():
    latest_status = Status.query.order_by(Status.id.desc()).first()
    decoder = json.JSONDecoder(object_pairs_hook=OrderedDict)

    return jsonify(decoder.decode(latest_status.json))
