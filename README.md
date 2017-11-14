# steamstatus
A simple &amp; open-source Steam monitoring service built with Flask.

## Dependencies
* Flask
* Flask-SQLAlchemy
* jQuery
* Bootstrap 4

## Deployment
1. Clone the repository

        git clone https://github.com/akelsch/steamstatus.git

2. Activate the virtual environment

        cd steamstatus
        source bin/activate

3. Set Flask environment variables

        export FLASK_APP=app.py
        export FLASK_DEBUG=1  // optional

4. Insert your [Steam Web API Key](https://steamcommunity.com/dev/apikey) in app.py

5. Run the app

        cd src
        flask run
