# steamstatus

A Steam monitoring service built with Flask

<img src="https://raw.githubusercontent.com/akelsch/steamstatus/master/screenshot.png" width="720">

## Requirements

- Python 3.4+
- A modern browser

## Installation: Linux & macOS

1. Clone the repository

    ```Shell
    git clone https://github.com/akelsch/steamstatus.git
    ```

2. Create a virtual environment and install all required packages

    ```Shell
    cd steamstatus && python -m venv venv
    source venv/bin/activate && pip install -r requirements.txt
    ```

    See [`requirements.txt`](https://github.com/akelsch/steamstatus/blob/master/requirements.txt) for a complete list of required packages

3. Set Flask environment variables

    ```Shell
    export FLASK_APP=app.py
    export FLASK_DEBUG=1 # optional
    ```

4. **Insert your [Steam Web API key](https://steamcommunity.com/dev/apikey) in configuration.py**

5. Run the app

    ```Shell
    cd src
    flask run
    ```

## Installation: Windows

PowerShell commands differ quite a bit from Bash so here are some equivalent commands:

```PowerShell
# source venv/bin/activate
.\venv\Scripts\Activate.ps1

# export FLASK_APP=app.py
$env:FLASK_APP="app.py"
```

Please note that running scripts in PowerShell requires changing your execution policy to `Unrestricted` (see [Set-ExecutionPolicy](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.security/set-executionpolicy?view=powershell-6)).

You will also need to use three instead of four leading slashes for the database URI (see [SQLAlchemy docs](http://docs.sqlalchemy.org/en/latest/core/engines.html#sqlite)).

## Acknowledgments

Flag icons by [Mark James](http://www.famfamfam.com/lab/icons/flags/)
