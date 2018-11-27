from flask import Flask
from flask_restful import Api,Resource
from models.base import db
from resources.counterAPI import CounterAPI
import pymysql
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_SCHEMA

app = Flask(__name__)
api = Api(app)


#app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://{}:{}@{}:{}/{}".format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_SCHEMA)
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#db.init_app(app)
#with app.app_context():
    #db.create_all()


class Main_goodinfo(Resource):
    @staticmethod
    def get():
        db = pymysql.connect(host='127.0.0.1', user='root', password='mm5201314', database='petcamp', port=3306,
                             charset='utf8', cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()
        cursor.execute("select * from goodinfo")
        data = cursor.fetchall()
        datanew = {}
        print(datanew)
        datanew["msg"] = data
        return datanew, 200, {"Access-Control-Allow-Origin": "*"}


api.add_resource(Main_goodinfo, "/api/maingoodinfo")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
