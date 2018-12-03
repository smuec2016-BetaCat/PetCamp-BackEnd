from models.base import db


agency_image = db.Table(
    "agency_image",
    db.Column("agency_id", db.Integer, db.ForeignKey("agency.id"), primary_key=True),
    db.Column("image_id", db.Integer, db.ForeignKey("image.id"), primary_key=True)
)

trust_order_image = db.Table(
    "trust_order_image",
    db.Column("order_id", db.Integer, db.ForeignKey("trusteeship_order.id"), primary_key=True),
    db.Column("image_id", db.Integer, db.ForeignKey("image.id"), primary_key=True)
)
