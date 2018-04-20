import json
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

from configuration import APIKEY
from utils import create_json

db = SQLAlchemy()

TABLENAME = "Status"


class Status(db.Model):
    """
    Database layout for storing statuses.
    """
    __tablename__ = TABLENAME

    timestamp = db.Column(db.DateTime, primary_key=True)
    json = db.Column(db.Text, nullable=False)


def create_table():
    """
    Function to create the status table.
    This is useful when running the app for the first time.
    """
    if not db.engine.dialect.has_table(db.engine, TABLENAME):
        db.create_all()


def update_database():
    """
    Function to update the database.
    """
    new_status = Status(timestamp=datetime.utcnow(), json=json.dumps(create_json(APIKEY)))
    db.session.add(new_status)
    db.session.commit()
