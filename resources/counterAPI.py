from flask_restful import Resource
from models.counter import Counter, db
import datetime


class CounterAPI(Resource):
    @staticmethod
    def get():
        return {"count": len(Counter.query.all())}, 200, {"Access-Control-Allow-Origin": "*"}

    @staticmethod
    def post():
        current_datetime = datetime.datetime.now()
        visit = Counter(date_time=current_datetime)
        db.session.add(visit)
        db.session.commit()
        return {"insert_time": current_datetime.strftime("%Y-%m-%d %H:%M:%S")}, 200, {"Access-Control-Allow-Origin": "*"}
