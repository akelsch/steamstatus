import json

from app import db
from models import Status
from status import create_json


def init_db():
    db.drop_all()
    db.create_all()


def update_db():
    new_status = Status(json=json.dumps(create_json()))
    db.session.add(new_status)
    db.session.commit()
