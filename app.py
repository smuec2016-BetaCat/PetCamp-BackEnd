from flask import Flask
from flask_restful import Api
from models.base import db
from resources.counterAPI import CounterAPI
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_SCHEMA

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://{}:{}@{}:{}/{}".format(
    DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_SCHEMA
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
with app.app_context():
    db.create_all()

api.add_resource(CounterAPI, "/api/v0/counter")

if __name__ == '__main__':
    app.run(host="0.0.0.0")
