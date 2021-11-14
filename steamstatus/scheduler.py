from flask import Flask
from flask_apscheduler import APScheduler

from steamstatus.service import update_status

scheduler = APScheduler()


def update_job():
    with scheduler.app.app_context():
        update_status()


def init_app(app: Flask):
    scheduler.init_app(app)
    scheduler.start()

    @app.before_first_request
    def before_first_request():
        update_status()
        scheduler.add_job("update_job", update_job, trigger="interval", seconds=app.config.get("UPDATE_FREQUENCY"))
