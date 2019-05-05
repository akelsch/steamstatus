import json
from datetime import datetime

from app import db
from config import API_KEY
from models import Status
from utils import create_json


def init_db():
    db.drop_all()
    db.create_all()


def update_db():
    new_status = Status(timestamp=datetime.utcnow(), json=json.dumps(create_json(API_KEY)))
    db.session.add(new_status)
    db.session.commit()
