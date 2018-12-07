from flask import request
from flask_restful import Resource
from models.image import Image
# from models.secondary import trust_order_image
from models.trusteeshipOrder import TrusteeshipOrder, db
# from models.agency import Agency
from models.base import to_dict
from datetime import datetime
import random

acao = {"Access-Control-Allow-Origin": "*"}


class TrusteeshipOrderAPI(Resource):
    """
    Trusteeship order API
    """
    @staticmethod
    def post():
        """
        Create a new order
        :return: success or error and the order number, failed image names
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
        order.ord_num = str(
            order.create_time.strftime("%Y%m%d%H%M%S")
            ) + "".join(
            [str(random.randint(0, 9)) for i in range(6)]
        )
        if "image_names" in json:
            for image_name in json["image_names"]:
                image = Image.query.filter_by(name=image_name).first()
                if image is None:
                    return {
                        "error": image_name + " not found in image table"
                        }, 404, acao
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
        order = TrusteeshipOrder.query.filter_by(
            ord_num=json["ord_num"]
            ).first()
        if order is None:
            return {"error": "Order not found"}, 404, acao
        try:
            order.agency_fee = json["agency_fee"]
        except KeyError:
            return {"error": "Agency fee is not provided"}, 406, acao
        order.close_time = datetime.now()
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
        if "agency_id" not in args and "ord_num" not in args:
            return {
                "error": "Either agency ID or order number must be provided"
                }, 406, acao
        if "ord_num" not in args:
            orders = TrusteeshipOrder.query.all()
            for i in range(len(orders)):
                orders[i] = to_dict(orders[i])
            return {"orders": orders}, 200, acao
        order = TrusteeshipOrder.query.filter_by(
            ord_num=args["ord_num"]
            ).first()
        if order is None:
            return {"error": "Order number doesn't exist"}, 404, acao
        return {"order": to_dict(order)}, 200, acao
