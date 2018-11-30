from flask import request
from flask_restful import Resource
from models.agency import Agency
from models.base import to_dict

acao = {"Access-Control-Allow-Origin": "*"}


class AgencyAPI(Resource):
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
            return {"agency_list": agency_list}, 200, acao
        agency = Agency.query.get(id=args["id"])
        if agency is None:
            return {"error": "Agency ID doesn't exist"}, 404, acao
        return {"agency": to_dict(agency)}, 200, acao
