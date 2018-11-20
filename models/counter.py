from models.base import db


class Counter(db.Model):
    id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True, unique=True)
    date_time = db.Column(db.DateTime, nullable=False)
