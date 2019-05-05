import json

from flask import jsonify, render_template

from app import app
from models import Status


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/status.json")
def status():
    latest_status = Status.query.order_by(Status.id.desc()).first()
    return jsonify(json.loads(latest_status.json))
