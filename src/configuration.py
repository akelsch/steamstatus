import os

# You can get your Steam Web API key here: https://steamcommunity.com/dev/apikey
APIKEY = ""

# Database location
BASEDIR = os.path.abspath(os.path.dirname(__file__))
DB_FILE = "app.db"
DB_LOCATION = os.path.join(BASEDIR, DB_FILE)

# Database update frequency in seconds
UPDATE_FREQUENCY = 10
