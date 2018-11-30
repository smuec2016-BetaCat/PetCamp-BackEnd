from flask import request
from flask_restful import Resource
from models.user import User, db
import datetime

acao = {"Access-Control-Allow-Origin": "*"}


class RegisterAPI(Resource):
    """
    Register API
    """
    @staticmethod
    def post():
        """
        Register
        :return: success or error message
        """
        username = request.json.get("username")
        password = request.json.get("password")
        if User.query.filter_by(username=username).first() is not None:
            return {"error": "User name has already been taken."}, 403, acao
        user = User(username=username, create_time=datetime.datetime.now())
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        return {"msg": "Success"}, 201, acao
