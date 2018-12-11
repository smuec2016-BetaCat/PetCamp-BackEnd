from flask import request, g
from flask_restful import Resource
from models.comment import Comment, db
from models.user import User
from models.base import to_dict
from datetime import datetime
from resources.authAPI import auth


class CommentAPI(Resource):
    """
    Comment API
    """
    decorators = [auth.login_required]

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
                agency_id=json["agency_id"]
            )
        except KeyError:
            return {"error": "Lack necessary argument"}, 406
        if g.current_user is None:
            return {"error": "Authorization problem"}, 401
        comment.user_id = g.current_user.id
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
            user = User.query.filter_by(id=comments[i].user_id).first()
            comments[i] = to_dict(comments[i])
            comments[i]["user_name"] = user.username
        return {"comments": comments}, 200
