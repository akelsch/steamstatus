# steamstatus
A simple &amp; open-source Steam monitoring service built with Flask.

<img src="https://raw.githubusercontent.com/akelsch/steamstatus/master/screenshot.png" width="720">

## Dependencies
This project is using the JavaScript Fetch API to consume JSON served by Flask (see [requirements.txt](https://github.com/akelsch/steamstatus/blob/master/requirements.txt) for a complete list of Python packages). The design is made with Bootstrap 4.

## Deployment (Unix & Mac)
1. Clone the repository

        git clone https://github.com/akelsch/steamstatus.git

2. Create a virtual environment and install all required packages

        cd steamstatus && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt

3. Set Flask environment variables

        export FLASK_APP=app.py
        export FLASK_DEBUG=1 // optional

4. Insert your [Steam Web API key](https://steamcommunity.com/dev/apikey) in configuration.py

5. Run the app

        cd src
        flask run

Note: Use three instead of four leading slashes for the database URI on Windows (see [SQLAlchemy docs](http://docs.sqlalchemy.org/en/latest/core/engines.html#sqlite)).
