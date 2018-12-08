from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_uploads import IMAGES, configure_uploads

from config import (DB_HOST, DB_PASSWORD, DB_PORT, DB_SCHEMA, DB_USER,
                    SECRET_KEY)
from models.base import db
from resources import (agencyAPI, authAPI, counterAPI, imageAPI, registerAPI,
                       trusteeshipOrderAPI, commentAPI, cartAPI, alipayAPI)
from resources.imageAPI import images

app = Flask(__name__)
CORS(app)
app.secret_key = SECRET_KEY
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = \
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_SCHEMA}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['UPLOADED_IMAGE_DEST'] = "./static/images"
app.config['UPLOADED_IMAGE_ALLOW'] = IMAGES
configure_uploads(app, images)

db.init_app(app)
with app.app_context():
    db.create_all()

api.add_resource(counterAPI.CounterAPI, "/api/v0/counter")
api.add_resource(registerAPI.RegisterAPI, "/api/v0/register")
api.add_resource(authAPI.AuthAPI, "/api/v0/auth")
api.add_resource(imageAPI.ImageAPI, "/api/v0/image")
api.add_resource(
    trusteeshipOrderAPI.TrusteeshipOrderAPI, "/api/v0/order/trusteeship"
    )
api.add_resource(agencyAPI.AgencyAPI, "/api/v0/agency")
api.add_resource(commentAPI.CommentAPI, "/api/v0/agency/comments")
api.add_resource(cartAPI.CartAPI, "/api/v0/cart")
api.add_resource(alipayAPI.AliPayAPI, "/api/v0/order/alipay")

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
