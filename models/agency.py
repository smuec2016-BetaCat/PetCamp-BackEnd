from models.base import db


class Agency(db.Model):
    """
    The model of agency
    """
    id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True, unique=True)
    name = db.Column(db.String(50), nullable=False)
    certification = db.Column(db.Boolean, nullable=False, default=False)
    create_time = db.Column(db.DateTime, nullable=False)
    trust_orders = db.relationship("TrusteeshipOrder", backref='agency')
