import os

# You can get your Steam Web API key here: https://steamcommunity.com/dev/apikey
APIKEY = ""

# Update frequency in seconds
UPDATE_FREQUENCY = 60

# Database URI
DB_SCHEMA = "sqlite:///" if os.name == "nt" else "sqlite:////"

APP_PATH = os.path.abspath(os.path.dirname(__file__))
DB_FILENAME = "app.db"
DB_PATH = os.path.join(APP_PATH, DB_FILENAME)

DB_URI = DB_SCHEMA + DB_PATH
