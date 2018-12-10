from models.base import db


class Image(db.Model):
    """
    The model of images
    """
    id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True, unique=True)
    name = db.Column(db.String(50), nullable=False)
    physical_name = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(250), nullable=False)
    upload_time = db.Column(db.DateTime, nullable=False)
    agency_avator = db.relationship("Agency", backref='avator_of')
