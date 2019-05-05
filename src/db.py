import json
from datetime import datetime

from app import db
from configuration import APIKEY
from models import Status
from utils import create_json


def init_db():
    db.drop_all()
    db.create_all()


def update_db():
    new_status = Status(timestamp=datetime.utcnow(), json=json.dumps(create_json(APIKEY)))
    db.session.add(new_status)
    db.session.commit()
