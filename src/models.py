from app import db


class Status(db.Model):
    __tablename__ = "Status"

    timestamp = db.Column(db.DateTime, primary_key=True)
    json = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return "<Status {}>".format(self.timestamp)
