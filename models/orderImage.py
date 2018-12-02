from models.base import db


trust_order_image = db.Table(
    "trust_order_image",
    db.Column("order_id", db.Integer, db.ForeignKey("trusteeship_order.id"), primary_key=True),
    db.Column("image_id", db.Integer, db.ForeignKey("image.id"), primary_key=True)
)

adoption_order_image = db.Table(
    "adoption_order_image",
    db.Column("order_id", db.Integer, db.ForeignKey("adoption_order.id"), primary_key=True),
    db.Column("image_id", db.Integer, db.ForeignKey("image.id"), primary_key=True)
)
