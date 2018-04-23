import json
import time
from collections import OrderedDict
from datetime import datetime
from urllib.error import URLError, HTTPError
from urllib.request import urlopen

from flask import abort

from app import db
from configuration import APIKEY
from models import Status

# Constants
STORE_URL = "https://store.steampowered.com/"
COMMUNITY_URL = "http://steamcommunity.com/"
API_URL = "https://api.steampowered.com/ISteamWebAPIUtil/GetServerInfo/v1/"
LOCATIONS = [
    "Australia", "Brazil", "Chile", "China Guangzhou", "China Shanghai", "China Tianjin", "Emirates", "EU East",
    "EU North", "EU West", "Hong Kong", "India", "India East", "Japan", "Peru", "Poland", "Singapore", "South Africa",
    "Spain", "US Northcentral", "US Northeast", "US Northwest", "US Southeast", "US Southwest"
]


def create_json(apikey):
    """
    Function to recreate the content of status.json from scratch.

    :param apikey: your Steam Web API key
    :return: the new status.json contents
    """
    print("[INFO] Starting status update")
    start = time.time()

    final_json = OrderedDict()
    csgo_json, steam_json, store_status, community_status, api_status = fetch_all(apikey)

    final_json["steam"] = OrderedDict()
    final_json["steam"]["online"] = steam_json["response"]["player_count"]

    final_json["steam"]["services"] = OrderedDict()
    final_json["steam"]["services"]["store"] = store_status
    final_json["steam"]["services"]["community"] = community_status
    final_json["steam"]["services"]["api"] = api_status

    final_json["csgo"] = OrderedDict()
    final_json["csgo"]["services"] = OrderedDict()
    final_json["csgo"]["services"]["sessions_logon"] = csgo_json["result"]["services"]["SessionsLogon"]
    final_json["csgo"]["services"]["player_inventories"] = csgo_json["result"]["services"]["SteamCommunity"]
    final_json["csgo"]["services"]["matchmaking_scheduler"] = csgo_json["result"]["matchmaking"]["scheduler"]

    final_json["csgo"]["servers"] = OrderedDict()
    for location in LOCATIONS:
        final_json["csgo"]["servers"][location] = csgo_json["result"]["datacenters"][location]["load"]

    end = time.time()
    print("[INFO] Finished status update in {:.2f} seconds".format(end - start))

    return final_json


def fetch_all(apikey):
    """
    Fetches all the necessary data we need to build our status.json file.

    :param apikey: your Steam Web API key
    :return: the fetched data
    """
    # Services
    steam_url = "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid=0"
    steam_json = fetch_json(steam_url)

    store_status = fetch_http_code(STORE_URL)
    community_status = fetch_http_code(COMMUNITY_URL)
    api_status = fetch_http_code(API_URL)

    # CS:GO Servers
    csgo_url = "https://api.steampowered.com/ICSGOServers_730/GetGameServersStatus/v1/?key=" + apikey
    csgo_json = fetch_json(csgo_url)

    return csgo_json, steam_json, store_status, community_status, api_status


def fetch_http_code(url):
    """
    Get the HTTP status code of a given URL.

    :param url: URL to check the HTTP status code of
    :return: an HTTP status code or "offline"
    """
    print("[INFO] Fetching HTTP status code of '{}'".format(url))

    try:
        return urlopen(url).getcode()
    except HTTPError as e:
        return e.code
    except URLError:
        return "offline"


def fetch_json(url):
    """
    Fetch JSON from the given URL.

    :param url: URL to fetch JSON from
    :return: the fetched JSON or an error page
    """
    print("[INFO] Fetching JSON from '{}'".format(url))

    try:
        return json.loads(urlopen(url).read().decode())
    except HTTPError as e:
        abort(e.code, description="Did you remember to enter your Steam Web API key?")
    except URLError:
        abort(503, description="The Steam Web API can not be reached.")


def init_db():
    """
    Function to create the status table.
    This is useful when running the app for the first time.
    """
    if not db.engine.dialect.has_table(db.engine, "Status"):
        db.create_all()


def update_db():
    """
    Function to update the database.
    """
    new_status = Status(timestamp=datetime.utcnow(), json=json.dumps(create_json(APIKEY)))
    db.session.add(new_status)
    db.session.commit()
