from flask import request
from flask_restful import Resource
from models.comment import Comment, db
from models.base import to_dict
from datetime import datetime


class CommentAPI(Resource):
    """
    Comment API
    """
    @staticmethod
    def post():
        """
        Add comment
        :return: success or error message
        """
        json = request.get_json()
        try:
            comment = Comment(
                content=json["content"],
                rank=json["rank"],
                create_time=datetime.now(),
                user_id=json["user_id"],
                agency_id=json["agency_id"]
            )
        except KeyError:
            return {"error": "Lack necessary argument"}, 406
        db.session.add(comment)
        db.session.commit()
        return {"msg": "Success", "comment": to_dict(comment)}, 201

    @staticmethod
    def get():
        """
        Get comments
        :return: comments or error message
        """
        args = request.args
        try:
            comments = Comment.query.filter_by(
                agency_id=args["agency_id"]
                ).all()
        except KeyError:
            return {"error": "Lack necessary argument"}, 406
        for i in range(len(comments)):
            comments[i] = to_dict(comments[i])
        return {"comments": comments}, 200
