from models.base import db
from models.orderImage import adoption_order_image


class AdoptionOrder(db.Model):
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
    address = db.Column(db.String(50), nullable=False)
    reason = db.Column(db.String(50), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    close_time = db.Column(db.DateTime)
    images = db.relationship(
        "Image",
        secondary=adoption_order_image,
        lazy='subquery',
        backref=db.backref('order', lazy=True)
    )