from models.base import db


class Comment(db.Model):
    """
    The model of user comments
    """
    id = db.Column(
        db.Integer,
        autoincrement=True,
        nullable=False,
        primary_key=True,
        unique=True
        )
    content = db.Column(db.Text, nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
        )
    agency_id = db.Column(
        db.Integer,
        db.ForeignKey("agency.id"),
        nullable=False
        )
