import json
import urllib.request

from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Insert API Key here
    key = 'XXX'
    url = 'https://api.steampowered.com/ICSGOServers_730/GetGameServersStatus/v1/?key=' + key

    # Fetch data from Steam API
    with urllib.request.urlopen(url) as response:
        data = response.read()

    # Prettify JSON
    status = json.loads(data.decode('utf-8'))
    status = str(json.dumps(status, indent=4))

    return render_template('index.html', status=status)
