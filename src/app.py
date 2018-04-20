import json
import os
from collections import OrderedDict

from flask import Flask, jsonify, render_template

from database import Status, db, create_table, update_database

app = Flask(__name__)

app.before_first_request_funcs = [create_table, update_database]

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["JSON_SORT_KEYS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/status.json", methods=["GET"])
def status():
    last_status = Status.query.order_by(Status.timestamp.desc()).limit(1).first()
    decoder = json.JSONDecoder(object_pairs_hook=OrderedDict)

    return jsonify(decoder.decode(last_status.json))
