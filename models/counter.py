from models.base import db


class Counter(db.Model):
    """
    The model of counter
    """
    id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True, unique=True)
    date_time = db.Column(db.DateTime, nullable=False)
    agency_id = db.Column(db.Integer, db.ForeignKey("agency.id"), nullable=False)
