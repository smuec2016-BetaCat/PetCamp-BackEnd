from flask import Flask
from flask_restful import Api
from flask_uploads import IMAGES, configure_uploads
from models.base import db
from resources import *
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_SCHEMA, SECRET_KEY
from resources.imageAPI import images

app = Flask(__name__)
app.secret_key = SECRET_KEY
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://{}:{}@{}:{}/{}".format(
    DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_SCHEMA
)
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

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
