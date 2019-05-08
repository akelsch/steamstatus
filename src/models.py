from datetime import datetime

from app import db


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    data = db.Column(db.JSON, nullable=False)

    def __repr__(self):
        return "<Status(id={}, timestamp={})>".format(self.id, self.timestamp)
