from flask_restful import Resource
from models.counter import Counter, db
from resources.authAPI import auth
import datetime

acao = {"Access-Control-Allow-Origin": "*"}


class CounterAPI(Resource):
    """
    Counter API
    """
    decorators = [auth.login_required]

    @staticmethod
    def get():
        """
        Get the number of records
        :return: the number of records
        """
        return {"count": len(Counter.query.all())}, 200, acao

    @staticmethod
    def post():
        """
        Insert a new record
        :return: insert time
        """
        current_datetime = datetime.datetime.now()
        visit = Counter(date_time=current_datetime)
        db.session.add(visit)
        db.session.commit()
        return {
                   "insert_time": current_datetime.strftime("%Y-%m-%d %H:%M:%S")
               }, 200, acao

    @staticmethod
    def delete():
        """
        Clear all records in the datatable
        :return: The number of deleted rows
        """
        deleted_rows = Counter.query.delete()
        db.session.commit()
        return {"deleted_rows": deleted_rows}, 200, acao
