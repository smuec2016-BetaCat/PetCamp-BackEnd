from models.base import db
from models.orderImage import trust_order_image


class TrusteeshipOrder(db.Model):
    """
    The model of trusteeship orders
    """
    id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True, unique=True)
    ord_num = db.Column(db.String(30), nullable=False)
    species = db.Column(db.String(50), nullable=False)
    pet_name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    expiration = db.Column(db.Integer, nullable=False)
    sterilization = db.Column(db.Boolean, nullable=False)
    naughty = db.Column(db.Boolean)
    shy = db.Column(db.Boolean)
    friendly = db.Column(db.Boolean)
    comment = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    close_time = db.Column(db.DateTime)
    agency_fee = db.Column(db.Float)
    agency_id = db.Column(db.Integer, db.ForeignKey('agency.id'), nullable=False)
    images = db.relationship(
        "Image",
        secondary=trust_order_image,
        lazy='subquery',
        backref=db.backref('order', lazy=True)
    )
