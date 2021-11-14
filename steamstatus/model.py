from datetime import datetime

from steamstatus.db import db


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    data = db.Column(db.JSON, nullable=False)

    def __repr__(self):
        return f"<Status(id={self.id}, timestamp={self.timestamp})>"


class Flag():
    def __init__(self, name: str, code: str, plural: bool = False):
        self.name = name
        self.img = f"img/flags/{code}.gif"
        self.plural = plural

    def __repr__(self):
        if self.plural:
            return f"Flag of the {self.name}"
        return f"Flag of {self.name}"


class Region():
    def __init__(self, name: str, flag: Flag):
        self.id = name.lower().replace(" ", "-")
        self.name = name
        self.flag = flag

    def __repr__(self):
        return self.name
