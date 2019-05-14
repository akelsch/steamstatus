import requests

from steamstatus.config import API_KEY, REQUESTS_TIMEOUT

ONLINE_USERS_URL = "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid=0"
STORE_URL = "https://store.steampowered.com/"
COMMUNITY_URL = "https://steamcommunity.com/"
WEB_API_URL = "https://api.steampowered.com/ISteamWebAPIUtil/GetServerInfo/v1/"
CSGO_URL = "https://api.steampowered.com/ICSGOServers_730/GetGameServersStatus/v1/?key=" + API_KEY


def create_new_status():
    """Creates status.json from scratch."""
    csgo_json = get_json(CSGO_URL)["result"]

    status = {
        "steam": {
            "online": get_json(ONLINE_USERS_URL)["response"]["player_count"],
            "services": {
                "store": get_status_code(STORE_URL),
                "community": get_status_code(COMMUNITY_URL),
                "webApi": get_status_code(WEB_API_URL)
            }
        },
        "csgo": {
            "online": csgo_json["matchmaking"]["online_players"],
            "services": {
                "sessionsLogon": csgo_json["services"]["SessionsLogon"],
                "playerInventories": csgo_json["services"]["SteamCommunity"],
                "matchmakingScheduler": csgo_json["matchmaking"]["scheduler"]
            },
            "servers": {
            }
        }
    }

    # Capitalize csgo services values
    status["csgo"]["services"] = {k: v.capitalize() for k, v in status["csgo"]["services"].items()}

    # Fill csgo servers load values, also capitalized
    status["csgo"]["servers"] = {k: v["load"].capitalize() for k, v in csgo_json["datacenters"].items()}

    return status


def get_json(url):
    """Makes a request to a given URL and returns the response JSON data."""
    response = requests.get(url)
    return response.json()


def get_status_code(url):
    """Makes a request to a given URL and returns the response status code."""
    try:
        response = requests.get(url, timeout=REQUESTS_TIMEOUT)
    except requests.exceptions.RequestException as e:
        return 503

    return response.status_code
