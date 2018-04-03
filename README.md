# steamstatus
A simple &amp; open-source Steam monitoring service built with Flask.

<img src="https://raw.githubusercontent.com/akelsch/steamstatus/master/readme.png" width="720">

## Dependencies
This project is built with Flask. It is using Bootstrap 4 for the design and jQuery to consume the JSON served by Flask. See [requirements.txt](https://github.com/akelsch/steamstatus/blob/master/requirements.txt) for a complete list of Python packages.

## Deployment (Unix / Mac)
1. Clone the repository

        git clone https://github.com/akelsch/steamstatus.git

2. Create a virtual environment and install all required packages

        virtualenv steamstatus && cd steamstatus && source bin/activate && pip install -r requirements.txt

3. Set Flask environment variables

        export FLASK_APP=app.py
        export FLASK_DEBUG=1  // optional

4. Insert your [Steam Web API Key](https://steamcommunity.com/dev/apikey) in app.py (search for APIKEY)

5. Run the app

        cd src
        flask run

Note: Use three leading slashes for the database URI on Windows (see [SQLAlchemy docs](http://docs.sqlalchemy.org/en/latest/core/engines.html#sqlite))
