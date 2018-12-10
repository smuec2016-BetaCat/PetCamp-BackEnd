from flask import request, g
from flask_restful import Resource
from authAPI import verify_admin
from models.agency import Agency, db
from models.user import User
from models.base import to_dict
from datetime import datetime


class AgencyAPI(Resource):
    @staticmethod
    def post():
        """
        Create a new agency
        :return: success or error message
        """
        json = request.get_json()
        try:
            agency = Agency(
                name=json["name"],
                introduction=json["introduction"],
                city=json["city"],
                address=json["address"],
                phone=json["phone"],
                create_time=datetime.now(),
                avator = json["avator"]
            )
            manager_id = json["manager_id"]
        except KeyError:
            return {"error": "Lack necessary argument"}, 406
        if g.current_user.id != manager_id and verify_admin() == False:
            return {"error": "Authorization problem"}, 401
        if Agency.query.filter_by(name=json["name"]).first() is not None:
            return {"error": "Agency name has been taken"}, 403
        agency.last_update = agency.create_time
        manager = User.query.filter_by(id=manager_id).first()
        if manager is None:
            return {"error": "User not found"}, 404
        if manager.own_agent_id is not None:
            return {"error": "User has been hired"}, 402
        db.session.add(agency)
        db.session.commit()
        agency = Agency.query.filter_by(name=json["name"]).first()
        manager.own_agent_id = agency.id
        db.session.commit()
        return {"msg": "Success"}, 201

    @staticmethod
    def put():
        """
        Change agency certification status
        :return: success or error message
        """
        json = request.get_json()
        try:
            agency.certification = json["certification"]
            id = json["id"]
        except KeyError:
            return {"error": "Lack necessary argument"}, 406

        if g.current_user.own_agent_id != id and verify_admin() == False:
            return {"error": "Authorization problem"}, 401
        
        agency = Agency.query.filter_by(id=id).first()
        if agency is None:
            return {"error": "Agency not found"}, 404
        agency.last_update = datetime.now()
        db.session.commit()
        return {"msg": "Success"}, 200

    @staticmethod
    def get():
        """
        Get agency information
        :return: agency information
        """
        args = request.args
        if "id" not in args:
            agency_list = Agency.query.all()
            for i in range(len(agency_list)):
                agency_list[i] = to_dict(agency_list[i])
            return {"agency_list": agency_list}, 200
        agency = Agency.query.get(int(args["id"]))
        if agency is None:
            return {"error": "Agency ID doesn't exist"}, 404
        return {"agency": to_dict(agency)}, 200

    @staticmethod
    def patch():
        """
        Add a new manager to agency
        :return: success or error message
        """
        json = request.get_json()
        try:
            manager = User.query.filter_by(username=json["username"]).first()
            agency_id = json["agency_id"]
        except KeyError:
            return {"error": "Lack necessary argument"}, 406

        if g.current_user.own_agent_id != agency_id and verify_admin() == False:
            return {"error": "Authorization problem"}, 401

        if manager is None:
            return {"error": "User not found"}, 404
        if manager.own_agent_id is not None:
            return {"error": "User has been hired"}, 402
        manager.own_agent_id = agency_id
        manager.own_agency.last_update = datetime.now()
        db.session.commit()
        return {"msg": "Success"}, 201

    @staticmethod
    def delete():
        """
        Remove a manager from agency
        :return: success or error message
        """
        json = request.get_json()
        try:
            manager = User.query.filter_by(username=json["username"]).first()
            agency_id = json["agency_id"]
        except KeyError:
            return {"error": "Lack necessary argument"}, 406

        if g.current_user.own_agent_id != agency_id and verify_admin() == False:
            return {"error": "Authorization problem"}, 401

        if manager is None:
            return {"error": "User not found"}, 404
        if manager.own_agent_id is None:
            return {"error": "User is free"}, 402
        if manager.own_agency.id != agency_id:
            return {"error": "User cannot be removed by a wrong agency"}, 403
        manager.own_agent_id = None
        manager.own_agency.last_update = datetime.now()
        db.session.commit()
        return {"msg": "Success"}, 200
