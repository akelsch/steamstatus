# steamstatus
A simple &amp; open-source Steam monitoring service built with Flask.

<img src="https://raw.githubusercontent.com/akelsch/steamstatus/master/readme.png" width="540">

## Dependencies
This project is built with Flask. It is using Bootstrap 4 for the design and jQuery to consume the JSON served by Flask. See requirements.txt for a complete list of Python packages.

## Deployment
1. Clone the repository

        git clone https://github.com/akelsch/steamstatus.git

2. Create a virtual environment and install all required packages

        virtualenv steamstatus && cd steamstatus && source bin/activate && pip install -r requirements.txt

3. Set Flask environment variables

        export FLASK_APP=app.py
        export FLASK_DEBUG=1  // optional

Note: Running Flask in debug mode will spawn two processes causing the update_database() function to run twice as well (see [Stack Overflow](https://stackoverflow.com/questions/25504149/why-does-running-the-flask-dev-server-run-itself-twice)).

4. Insert your [Steam Web API Key](https://steamcommunity.com/dev/apikey) in app.py

5. Run the app

        cd src
        flask run

## Potential improvements
* Store JSON in a better way
* Make use of historical data (e.g. uptime graph)
* And probably much more...
