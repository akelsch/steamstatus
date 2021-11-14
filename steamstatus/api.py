import requests
from flask import current_app as app

ONLINE_USERS_URL = "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid=0"
CSGO_URL = "https://api.steampowered.com/ICSGOServers_730/GetGameServersStatus/v1/?key={}"
STORE_URL = "https://store.steampowered.com/"
COMMUNITY_URL = "https://steamcommunity.com/"
WEB_API_URL = "https://api.steampowered.com/ISteamWebAPIUtil/GetServerInfo/v1/"


def create_new_status():
    """Creates status information from scratch."""
    csgo_url_with_key = CSGO_URL.format(app.config.get("API_KEY"))

    online_users_json = get_json(ONLINE_USERS_URL)["response"]
    csgo_json = get_json(csgo_url_with_key)["result"]
    store_status = get_status_code(STORE_URL)
    community_status = get_status_code(COMMUNITY_URL)
    webApi_status = get_status_code(WEB_API_URL)

    status = {
        "steam": {
            "online": online_users_json["player_count"],
            "services": {
                "store": store_status,
                "community": community_status,
                "webApi": webApi_status
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
        response = requests.get(url, timeout=app.config.get("REQUESTS_TIMEOUT"))
        return response.status_code
    except:
        return 503
