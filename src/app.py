from flask import Flask, abort, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

import json
import os
from collections import OrderedDict
from datetime import datetime, timedelta
from time import time
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////" + os.path.join(basedir, "app.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JSON_SORT_KEYS"] = False
db = SQLAlchemy(app)

# Database layout for storing statuses
class Status(db.Model):
    timestamp = db.Column(db.DateTime, primary_key=True)
    json = db.Column(db.Text, nullable=False)

# Helper function to fetch JSON from the given url
def fetch_json(url):
    try:
        return json.loads(urlopen(url).read().decode())
    except HTTPError as e:
        abort(e.code, description="There is something wrong with your parameters.")
    except URLError as e:
        abort(503, description="The Steam Web API can not be reached.")

# Helper function to get the HTTP code of a URL connection
def fetch_http_code(url):
    try:
        return urlopen(url).getcode()
    except HTTPError as e:
        return e.code
    except URLError as e:
        return "offline"

# Function to recreate JSON from scratch and save it to the database
def create_json():
    start = time()
    # Get all required JSON data from Steam
    key = "XXX"
    csgo_url = "https://api.steampowered.com/ICSGOServers_730/GetGameServersStatus/v1/?key=" + key
    steam_url = "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid=0"
    print(">>> Fetching JSON from '{}'".format(csgo_url))
    csgo_json = fetch_json(csgo_url)
    print(">>> Fetching JSON from '{}'".format(steam_url))
    steam_json = fetch_json(steam_url)

    # Additional service statuses by checking HTTP codes
    store_url = "https://store.steampowered.com/"
    community_url = "http://steamcommunity.com/"
    api_url = "https://api.steampowered.com/ISteamWebAPIUtil/GetServerInfo/v1/"
    print(">>> Fetching HTTP Status Code of '{}'".format(store_url))
    store_status = fetch_http_code(store_url)
    print(">>> Fetching HTTP Status Code of '{}'".format(community_url))
    community_status = fetch_http_code(community_url)
    print(">>> Fetching HTTP Status Code of '{}'".format(api_url))
    api_status = fetch_http_code(api_url)

    # Combine JSON using a ordered dict to remain order
    final_json = OrderedDict()
    final_json["steam_users"] = steam_json["response"]["player_count"]

    final_json["steam_services"] = OrderedDict()
    final_json["steam_services"]["store_status"] = store_status
    final_json["steam_services"]["community_status"] = community_status
    final_json["steam_services"]["api_status"] = api_status

    final_json["csgo_services"] = OrderedDict()
    final_json["csgo_services"]["csgo_sessions_logon"] = csgo_json["result"]["services"]["SessionsLogon"]
    final_json["csgo_services"]["csgo_player_inventories"] = csgo_json["result"]["services"]["SteamCommunity"]
    final_json["csgo_services"]["csgo_matchmaking_scheduler"] = csgo_json["result"]["matchmaking"]["scheduler"]

    final_json["csgo_servers"] = OrderedDict()
    server_locations = [
        "Australia", "Brazil", "Chile", "China Guangzhou", "China Shanghai", "China Tianjin",
        "Emirates", "EU East", "EU North", "EU West", "Hong Kong", "India",
        "India East", "Japan", "Peru", "Poland", "Singapore", "South Africa",
        "Spain", "US Northcentral", "US Northeast", "US Northwest", "US Southeast", "US Southwest"
    ]
    for location in server_locations:
        final_json["csgo_servers"][location] = csgo_json["result"]["datacenters"][location]["load"]

    # Save status to database
    final_status = Status(timestamp=datetime.utcnow(), json=json.dumps(final_json))
    db.session.add(final_status)
    db.session.commit()

    end = time()
    print(">>> Finished status update in {:.2f}s!".format(end - start))
    return final_json

@app.route("/status.json", methods=["GET"])
def steam_route():
    # Retrieve newest status entry from the database
    last_status = Status.query.order_by(Status.timestamp.desc()).limit(1).first()

    # Serve decoded JSON from the database if entry is not older than 60s
    if last_status.timestamp > datetime.utcnow() - timedelta(seconds=60):
        print(">>> Last status NOT older than 60s! Serving from database...")
        decoder = json.JSONDecoder(object_pairs_hook=OrderedDict)
        return jsonify(decoder.decode(last_status.json))

    # Else, create a new entry
    print(">>> Last status older than 60s! Updating entry...")
    return jsonify(create_json())

@app.route("/")
def index():
    return render_template("index.html")
