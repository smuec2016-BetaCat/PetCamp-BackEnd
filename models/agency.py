from models.base import db
from models.secondary import agency_image


class Agency(db.Model):
    """
    The model of agency
    """
    id = db.Column(
        db.Integer,
        autoincrement=True,
        nullable=False,
        primary_key=True,
        unique=True
        )
    name = db.Column(db.String(50), nullable=False)
    introduction = db.Column(db.Text, nullable=True)
    city = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    certification = db.Column(db.Boolean, nullable=False, default=False)
    create_time = db.Column(db.DateTime, nullable=False)
    last_update = db.Column(db.DateTime, nullable=True)
    trust_orders = db.relationship("TrusteeshipOrder", backref='agency')
    images = db.relationship(
        "Image",
        secondary=agency_image,
        lazy='subquery',
        backref=db.backref('image_of', lazy=True)
    )
    managers = db.relationship("User", backref="own_agency")
    comments = db.relationship("Comment", backref="comment_for")
