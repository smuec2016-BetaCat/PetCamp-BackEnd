from flask import request
from flask_restful import Resource
from models.trusteeshipOrder import TrusteeshipOrder, db
from models.base import to_dict
from datetime import datetime

acao = {"Access-Control-Allow-Origin": "*"}


class TrusteeshipOrderAPI(Resource):
    """
    Trusteeship order API
    """
    @staticmethod
    def put():
        """
        Close an order
        :return: success or error message and the close time
        """
        json = request.get_json()
        order = TrusteeshipOrder.query.filter_by(
            ord_num=json["ord_num"],
            status=1
            ).first()
        if order is None:
            return {"error": "Order not found"}, 404, acao
        try:
            order.agency_fee = json["agency_fee"]
        except KeyError:
            return {"error": "Agency fee is not provided"}, 406, acao
        order.status = 2
        order.close_time = datetime.now()
        db.session.commit()
        return {
            "msg": "Success",
            "close_time": order.close_time.strftime("%Y-%m-%d %H:%M:%S")
            }, 200, acao

    @staticmethod
    def get():
        """
        Get order information
        :return: order information
        """
        args = request.args
        if "ord_num" in args:
            order = TrusteeshipOrder.query.filter_by(
                ord_num=args["ord_num"],
                status=1
            ).first()
            if order is None:
                order = TrusteeshipOrder.query.filter_by(
                    ord_num=args["ord_num"],
                    status=2
                ).first()
                if order is None:
                    return {"error": "Order not found"}, 404, acao
            return {"order": to_dict(order)}, 200, acao

        elif "user_id" in args:
            orders = TrusteeshipOrder.query.filter_by(
                user_id=args["user_id"],
                status=1
            ).all()
            orders += TrusteeshipOrder.query.filter_by(
                user_id=args["user_id"],
                status=2
            ).all()
            if len(orders) == 0:
                return {"error": "Order not found"}, 404, acao

        elif "agency_id" in args:
            orders = TrusteeshipOrder.query.filter_by(
                agency_id=args["agency_id"],
                status=1
            ).all()
            orders += TrusteeshipOrder.query.filter_by(
                agency_id=args["agency_id"],
                status=2
            ).all()
            if len(orders) == 0:
                return {"error": "Order not found"}, 404, acao

        else:
            return {
                "error": "Agency ID, user ID or order number must be provided"
                }, 406, acao

        for i in range(len(orders)):
            orders[i] = to_dict(orders[i])
        return {"orders": orders}, 200, acao
