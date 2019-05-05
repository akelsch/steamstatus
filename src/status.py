import time
from collections import OrderedDict

import requests

from config import API_KEY

ONLINE_USERS_URL = "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid=0"
STORE_URL = "https://store.steampowered.com/"
COMMUNITY_URL = "https://steamcommunity.com/"
API_URL = "https://api.steampowered.com/ISteamWebAPIUtil/GetServerInfo/v1/"
CSGO_URL = "https://api.steampowered.com/ICSGOServers_730/GetGameServersStatus/v1/?key=" + API_KEY
LOCATIONS = [
    "Australia", "Brazil", "Chile",
    "China Guangzhou", "China Shanghai", "China Tianjin",
    "Emirates", "EU East", "EU North",
    "EU West", "Hong Kong", "India",
    "India East", "Japan", "Peru",
    "Poland", "Singapore", "South Africa",
    "Spain", "US Northcentral", "US Northeast",
    "US Northwest", "US Southeast", "US Southwest"
]


def create_json():
    """
    Creates status.json from scratch.
    """
    print("Starting status.json update...")
    start = time.time()

    steam_json = get_json(ONLINE_USERS_URL)
    csgo_json = get_json(CSGO_URL)

    # TODO find a better way to do this
    status = OrderedDict()
    status["steam"] = OrderedDict()
    status["steam"]["services"] = OrderedDict()
    status["csgo"] = OrderedDict()
    status["csgo"]["services"] = OrderedDict()
    status["csgo"]["servers"] = OrderedDict()

    # Services
    status["steam"]["online"] = steam_json["response"]["player_count"]
    status["steam"]["services"]["store"] = get_status_code(STORE_URL)
    status["steam"]["services"]["community"] = get_status_code(COMMUNITY_URL)
    status["steam"]["services"]["api"] = get_status_code(API_URL)

    # CS:GO Servers
    status["csgo"]["services"]["sessions_logon"] = csgo_json["result"]["services"]["SessionsLogon"]
    status["csgo"]["services"]["player_inventories"] = csgo_json["result"]["services"]["SteamCommunity"]
    status["csgo"]["services"]["matchmaking_scheduler"] = csgo_json["result"]["matchmaking"]["scheduler"]

    for location in LOCATIONS:
        status["csgo"]["servers"][location] = csgo_json["result"]["datacenters"][location]["load"]

    end = time.time()
    print("Finished update in {:.2f} seconds!".format(end - start))

    return status


def get_json(url):
    """
    Makes a request to a given URL and returns its JSON contents.
    """
    response = requests.get(url)
    return response.json()


def get_status_code(url):
    """
    Makes a request to a given URL and returns its status code.
    """
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        return "offline"

    return response.status_code