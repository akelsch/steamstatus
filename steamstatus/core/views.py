import time

from flask import jsonify, render_template

from steamstatus import app, db, scheduler
from steamstatus.config import UPDATE_FREQUENCY
from steamstatus.core import create_new_status
from steamstatus.core.models import Flag, Region, Status


def update_status():
    app.logger.info("Starting status.json update")
    t0 = time.perf_counter()

    new_status = Status(data=create_new_status())
    db.session.add(new_status)
    db.session.commit()

    t1 = time.perf_counter()
    app.logger.info("Finished update in %.2f seconds", t1 - t0)


@app.before_first_request
def init():
    # Update once & start scheduler
    update_status()
    scheduler.add_job(update_status, "interval", seconds=UPDATE_FREQUENCY)
    scheduler.start()


@app.route("/")
def index():
    return render_template("index.html", regions=REGIONS)


@app.route("/status.json")
def status():
    latest_status = Status.query.order_by(Status.id.desc()).first()
    return jsonify(latest_status.data)


EU_FLAG = Flag("European Union", "eu", True)
US_FLAG = Flag("United States", "us", True)
CHINA_FLAG = Flag("China", "cn")
INDIA_FLAG = Flag("India", "in")

REGIONS = {
    "eu": [
        Region("EU North", EU_FLAG),
        Region("EU East", EU_FLAG),
        Region("EU West", EU_FLAG)
    ],
    "us": [
        Region("US Northcentral", US_FLAG),
        Region("US Northeast", US_FLAG),
        Region("US Northwest", US_FLAG),
        Region("US Southeast", US_FLAG),
        Region("US Southwest", US_FLAG)
    ],
    "china": [
        Region("China Guangzhou", CHINA_FLAG),
        Region("China Shanghai", CHINA_FLAG),
        Region("China Tianjin", CHINA_FLAG)
    ],
    "other": [
        Region("Australia", Flag("Australia", "au")),
        Region("Brazil", Flag("Brazil", "br")),
        Region("Chile", Flag("Chile", "cl")),
        Region("Emirates", Flag("Emirates", "ae", True)),
        Region("Hong Kong", Flag("Hong Kong", "hk")),
        Region("India", INDIA_FLAG),
        Region("India East", INDIA_FLAG),
        Region("Japan", Flag("Japan", "jp")),
        Region("Peru", Flag("Peru", "pe")),
        Region("Poland", Flag("Poland", "pl")),
        Region("Singapore", Flag("Singapore", "sg")),
        Region("South Africa", Flag("South Africa", "za")),
        Region("Spain", Flag("Spain", "es"))
    ]
}
