import json
import time
from collections import OrderedDict
from urllib.error import URLError, HTTPError
from urllib.request import urlopen

from flask import abort


def fetch_json(url):
    """
    Function to fetch JSON from the given url.
    Returns an error page with status code 503 if the server is not reachable.
    """
    try:
        return json.loads(urlopen(url).read().decode())
    except HTTPError as e:
        abort(e.code, description="""There is something wrong with your parameters.
            Did you remember to enter your key?""")
    except URLError:
        abort(503, description="The Steam Web API can not be reached.")


def fetch_http_code(url):
    """
    Function to get the HTTP status code of a URL connection.
    Returns "offline" if server is not reachable.
    """
    try:
        return urlopen(url).getcode()
    except HTTPError as e:
        return e.code
    except URLError:
        return "offline"


def create_json(apikey):
    """
    Function to recreate the content of status.json from scratch
    """
    start = time.time()

    # Get all required JSON data from Steam
    csgo_url = "https://api.steampowered.com/ICSGOServers_730/GetGameServersStatus/v1/?key=" + apikey
    steam_url = "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid=0"

    print(">>> Fetching JSON from '{}'".format(csgo_url))
    csgo_json = fetch_json(csgo_url)

    print(">>> Fetching JSON from '{}'".format(steam_url))
    steam_json = fetch_json(steam_url)

    # Additional service statuses by checking HTTP status codes
    store_url = "https://store.steampowered.com/"
    community_url = "http://steamcommunity.com/"
    api_url = "https://api.steampowered.com/ISteamWebAPIUtil/GetServerInfo/v1/"

    print(">>> Fetching HTTP status code of '{}'".format(store_url))
    store_status = fetch_http_code(store_url)

    print(">>> Fetching HTTP status code of '{}'".format(community_url))
    community_status = fetch_http_code(community_url)

    print(">>> Fetching HTTP status code of '{}'".format(api_url))
    api_status = fetch_http_code(api_url)

    # Combine all gathered information using ordered dicts to remain order
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

    end = time.time()
    print(">>> Finished status update in {:.2f}s!".format(end - start))
    return final_json
