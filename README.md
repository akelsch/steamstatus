# steamstatus

A Steam monitoring service built with Flask

<img src="screenshot.png" width="720">

## Requirements

- Python 3.4+
- A modern browser supporting [async functions](https://caniuse.com/#feat=async-functions)

## Getting Started

1. Install

    ```Shell
    git clone https://github.com/akelsch/steamstatus.git && cd steamstatus
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

    See [`requirements.txt`](requirements.txt) for a complete list of required packages.

2. Configure

    [`steamstatus/config.py`](steamstatus/config.py):

    ```Python
    API_KEY = "" # insert your key here, e.g. 204BE844F017F63E40E2F3D820EB8E9E
    UPDATE_FREQUENCY = 60
    ```

    You can get your own Steam Web API key [here](https://steamcommunity.com/dev/apikey).

3. Run

    ```Shell
    export FLASK_APP=steamstatus
    export FLASK_ENV=development # optional
    flask init-db
    flask run
    ```

### Using Windows

PowerShell commands differ quite a bit from Bash so here are some equivalent commands:

```PowerShell
# source venv/bin/activate
.\venv\Scripts\Activate.ps1

# export FLASK_APP=steamstatus
$env:FLASK_APP = "steamstatus"

# export FLASK_ENV=development
$env:FLASK_ENV = "development"
```

Please note that running scripts in PowerShell requires changing your execution policy to `Unrestricted`
(see [Set-ExecutionPolicy](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.security/set-executionpolicy?view=powershell-6)).

## Acknowledgments

Flag icons by [Mark James](http://www.famfamfam.com/lab/icons/flags/)
