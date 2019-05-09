import time
from collections import OrderedDict

import requests

from app import app
from config import API_KEY

ONLINE_USERS_URL = "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid=0"
STORE_URL = "https://store.steampowered.com/"
COMMUNITY_URL = "https://steamcommunity.com/"
API_URL = "https://api.steampowered.com/ISteamWebAPIUtil/GetServerInfo/v1/"
CSGO_URL = "https://api.steampowered.com/ICSGOServers_730/GetGameServersStatus/v1/?key=" + API_KEY


def create_json():
    """Creates status.json from scratch."""
    app.logger.info("Starting status.json update")
    start = time.time()

    # TODO find a better way to do this
    status = OrderedDict()

    # Steam
    status["steam"] = OrderedDict()
    status["steam"]["online"] = get_json(ONLINE_USERS_URL)["response"]["player_count"]
    status["steam"]["services"] = OrderedDict()
    status["steam"]["services"]["store"] = get_status_code(STORE_URL)
    status["steam"]["services"]["community"] = get_status_code(COMMUNITY_URL)
    status["steam"]["services"]["api"] = get_status_code(API_URL)

    # CS:GO
    csgo_json = get_json(CSGO_URL)["result"]
    status["csgo"] = OrderedDict()
    status["csgo"]["online"] = csgo_json["matchmaking"]["online_players"]
    status["csgo"]["services"] = OrderedDict()
    status["csgo"]["services"]["sessions_logon"] = csgo_json["services"]["SessionsLogon"].capitalize()
    status["csgo"]["services"]["player_inventories"] = csgo_json["services"]["SteamCommunity"].capitalize()
    status["csgo"]["services"]["matchmaking_scheduler"] = csgo_json["matchmaking"]["scheduler"].capitalize()

    status["csgo"]["servers"] = OrderedDict()
    for location in csgo_json["datacenters"]:
        status["csgo"]["servers"][location] = csgo_json["datacenters"][location]["load"].capitalize()

    end = time.time()
    app.logger.info("Finished update in %.2f seconds", end - start)

    return status


def get_json(url):
    """Makes a request to a given URL and returns the response JSON data."""
    response = requests.get(url)
    return response.json()


def get_status_code(url):
    """Makes a request to a given URL and returns the response status code."""
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        return 503

    return response.status_code
