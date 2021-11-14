import time

from flask import current_app as app

from steamstatus.api import create_new_status
from steamstatus.db import db
from steamstatus.model import Status


def get_latest_status() -> Status:
    return Status.query.order_by(Status.id.desc()).first()


def update_status():
    app.logger.info("Starting status.json update")
    t0 = time.perf_counter()

    new_status = Status(data=create_new_status())
    db.session.add(new_status)
    db.session.commit()

    t1 = time.perf_counter()
    app.logger.info("Finished update in %.2f seconds", t1 - t0)
