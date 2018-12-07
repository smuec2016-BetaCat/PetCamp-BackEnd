from flask import request
from flask_restful import Resource
<<<<<<< HEAD
from models.image import Image
from models.secondary import trust_order_image
from models.trusteeshipOrder import TrusteeshipOrder, db
from models.agency import Agency
from models.base import to_dict
from datetime import datetime
import random
=======
from models.trusteeshipOrder import TrusteeshipOrder, db
from models.base import to_dict
from datetime import datetime
>>>>>>> dev-yyh

acao = {"Access-Control-Allow-Origin": "*"}


class TrusteeshipOrderAPI(Resource):
    """
    Trusteeship order API
    """
    @staticmethod
<<<<<<< HEAD
    def post():
        """
        Create a new order
        :return: success or error message and the order number, failed image names
        """
        json = request.get_json()
        try:
            order = TrusteeshipOrder(
                species=json["species"],
                pet_name=json["pet_name"],
                age=json["age"],
                weight=json["weight"],
                expiration=json["expiration"],
                sterilization=json["sterilization"],
                naughty=json["naughty"],
                shy=json["shy"],
                friendly=json["friendly"],
                comment=json["comment"],
                price=json["price"],
                create_time=datetime.now(),
                agency_id=json["agency_id"]
            )
        except KeyError:
            return {"error": "Lack necessary argument"}, 406, acao
        else:
            return {"error": "Agency ID doesn't exist"}, 403, acao
        order.ord_num = str(order.create_time.strftime("%Y%m%d%H%M%S")) + "".join(
            [str(random.randint(0, 9)) for i in range(6)]
        )
        if "image_names" in json:
            for image_name in json["image_names"]:
                image = Image.query.filter_by(name=image_name).first()
                if image is None:
                    return {"error": image_name + " not found in image table"}, 404, acao
                order.images.append(image)
        db.session.add(order)
        db.session.commit()
        return {"msg": "Success", "ord_num": order.ord_num}, 201, acao

    @staticmethod
    def put():
        """
        Close order
        :return: success or error message and the close time
        """
        json = request.get_json()
        order = TrusteeshipOrder.query.filter_by(ord_num=json["ord_num"]).first()
=======
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
>>>>>>> dev-yyh
        if order is None:
            return {"error": "Order not found"}, 404, acao
        try:
            order.agency_fee = json["agency_fee"]
        except KeyError:
            return {"error": "Agency fee is not provided"}, 406, acao
<<<<<<< HEAD
        order.close_time = datetime.now()
        return {"msg": "Success", "close_time": order.close_time.strftime("%Y-%m-%d %H:%M:%S")}, 200, acao
=======
        order.status = 2
        order.close_time = datetime.now()
        db.session.commit()
        return {
            "msg": "Success",
            "close_time": order.close_time.strftime("%Y-%m-%d %H:%M:%S")
            }, 200, acao
>>>>>>> dev-yyh

    @staticmethod
    def get():
        """
        Get order information
        :return: order information
        """
        args = request.args
<<<<<<< HEAD
        if "agency_id" not in args and "ord_num" not in args:
            return {"error": "Either agency ID or order number must be provided"}, 406, acao
        if "ord_num" not in args:
            orders = TrusteeshipOrder.query.all()
            for i in range(len(orders)):
                orders[i] = to_dict(orders[i])
            return {"orders": orders}, 200, acao
        order = TrusteeshipOrder.query.filter_by(ord_num=args["ord_num"]).first()
        if order is None:
            return {"error": "Order number doesn't exist"}, 404, acao
        return {"order": to_dict(order)}, 200, acao

=======
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
>>>>>>> dev-yyh
