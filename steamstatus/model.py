from datetime import datetime

from steamstatus.db import db


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    data = db.Column(db.JSON, nullable=False)

    def __repr__(self):
        return "<Status(id={}, timestamp={})>".format(self.id, self.timestamp)


class Flag():
    def __init__(self, name: str, img: str, plural: bool = False):
        self.name = name
        self.img = "img/flags/{}.gif".format(img)
        self.plural = plural

    def __repr__(self):
        if self.plural:
            return "Flag of the {}".format(self.name)
        return "Flag of {}".format(self.name)


class Region():
    def __init__(self, name: str, flag: Flag):
        self.id = name.lower().replace(" ", "-")
        self.name = name
        self.flag = flag

    def __repr__(self):
        return self.name
