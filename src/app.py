import json

from urllib.request import Request, urlopen
from urllib.error import URLError

from flask import Flask, jsonify, request, abort

app = Flask(__name__)

def make_request(url):
    # Fetch & return data from Steam Web API as JSON object
    req = Request(url)
    try:
        return json.loads(urlopen(req).read().decode())
    # Catch possible errors when using urlopen()
    except URLError as e:
        if hasattr(e, "code"):
            abort(e.code, description="There is something wrong with your parameters.")
        elif hasattr(e, "reason"):
            abort(503, description="The Steam Web API can not be reached.")

def csgo_status(key):
    url = "https://api.steampowered.com/ICSGOServers_730/GetGameServersStatus/v1/?key=" + key
    return make_request(url)

def steam_status():
    url = "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid=0"
    return make_request(url)

@app.route("/api/csgo/v1/", methods=["GET"])
def csgo_route():
    key = request.args.get("key")
    if not key:
        abort(403, description="Access is denied. Retrying will not help. Please verify your key= parameter.")
    return jsonify(csgo_status(key))

@app.route("/api/steam/v1/", methods=["GET"])
def steam_route():
    return jsonify(steam_status())
