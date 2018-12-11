from flask import request
from flask_restful import Resource
from models.counter import Counter, db
import datetime


class CounterAPI(Resource):
    """
    Counter API
    """
    @staticmethod
    def get():
        """
        Get the number of records
        :return: the number of records
        """
        args = request.args
        try:
            count = len(
                Counter.query.filter_by(agency_id=args["agency_id"]).all()
                )
        except KeyError:
            count = len(
                Counter.query.all()
                )
        return {"count": count}, 200

    @staticmethod
    def post():
        """
        Insert a new record
        :return: insert time
        """
        json = request.get_json()
        current_datetime = datetime.datetime.now()
        try:
            visit = Counter(
                date_time=current_datetime,
                agency_id=json["agency_id"]
                )
        except KeyError:
            return {"error": "Lack necessary argument"}, 406
        db.session.add(visit)
        db.session.commit()
        count = len(
                Counter.query.filter_by(agency_id=json["agency_id"]).all()
                )
        return {"count": count}, 201

