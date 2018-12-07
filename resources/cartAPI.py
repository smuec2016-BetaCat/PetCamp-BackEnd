import random
from flask import request
from flask_restful import Resource
from models.trusteeshipOrder import TrusteeshipOrder, db
from models.image import Image
from models.base import to_dict
from datetime import datetime

acao = {"Access-Control-Allow-Origin": "*"}


class CartAPI(Resource):
    """
    Cart API
    """
    @staticmethod
    def post():
        """
        Add new pre-order
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
                agency_id=json["agency_id"],
                user_id=json["user_id"]
            )
        except KeyError:
            return {"error": "Lack necessary argument"}, 406, acao
        ord_num = str(
            order.create_time.strftime("%Y%m%d%H%M%S")
            ) + "".join(
            [str(random.randint(0, 9)) for i in range(6)]
        )
        order.ord_num = ord_num
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
        return {"msg": "Success", "ord_num": ord_num}, 201, acao

    @staticmethod
    def get():
        """
        Get cart orders
        :return: orders or error message
        """
        args = request.args
        try:
            orders = TrusteeshipOrder.query.filter_by(
                user_id=args["user_id"],
                status=0
                ).all()
        except KeyError:
            return {"error": "Lack necessary argument"}, 406, acao
        for i in range(len(orders)):
            orders[i] = to_dict(orders[i])
        return {"orders": orders}, 200, acao

    @staticmethod
    def put():
        """
        Open an order
        :return: success or error message and the open time
        """
        json = request.get_json()
        try:
            order = TrusteeshipOrder.query.filter_by(
                ord_num=json["ord_num"],
                status=0
            ).first()
            if order is None:
                return {"error": "Order not found"}, 404, acao
        except KeyError:
            return {"error": "Agency fee is not provided"}, 406, acao
        order.status = 1
        order.open_time = datetime.now()
        db.session.commit()
        return {
            "msg": "Success",
            "open_time": order.open_time.strftime("%Y-%m-%d %H:%M:%S")
            }, 200, acao

    @staticmethod
    def delete():
        """
        Delete an order in cart
        :return: success or error message
        """
        json = request.get_json()
        try:
            order = TrusteeshipOrder.query.filter_by(
                ord_num=json["ord_num"],
                status=0
            ).first()
            if order is None:
                return {"error": "Order not found"}, 404, acao
        except KeyError:
            return {"error": "Agency fee is not provided"}, 406, acao
        db.session.delete(order)
        db.session.commit()
        return {"msg": "Success"}, 200, acao
