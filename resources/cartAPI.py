import random
from flask import request, g
from flask_restful import Resource
from resources.authAPI import verify_admin
from models.trusteeshipOrder import TrusteeshipOrder, db
from models.image import Image
from models.base import to_dict
from datetime import datetime
from resources.authAPI import auth


class CartAPI(Resource):
    """
    Cart API
    """
    decorators = [auth.login_required]

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
                agency_id=json["agency_id"]
            )
        except KeyError:
            return {"error": "Lack necessary argument"}, 406

        order.user_id = g.current_user.id

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
                        }, 404
                order.images.append(image)
        db.session.add(order)
        db.session.commit()
        return {"msg": "Success", "ord_num": ord_num}, 201

    @staticmethod
    def get():
        """
        Get cart orders
        :return: orders or error message
        """
        orders = TrusteeshipOrder.query.filter_by(
            user_id=g.current_user.id,
            status=0
            ).all()
        
        for i in range(len(orders)):
            orders[i] = to_dict(orders[i])
        return {"orders": orders}, 200

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
                return {"error": "Order not found"}, 404
            assert order.user_id == g.current_user.id
        except KeyError:
            return {"error": "Agency fee is not provided"}, 406
        except AssertionError:
            return {"error": "Authorization problem"}, 401
        order.status = 1
        order.open_time = datetime.now()
        db.session.commit()
        return {
            "msg": "Success",
            "open_time": order.open_time.strftime("%Y-%m-%d %H:%M:%S")
            }, 200

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
                return {"error": "Order not found"}, 404
            assert order.user_id == g.current_user.id
        except KeyError:
            return {"error": "Agency fee is not provided"}, 406
        except AssertionError:
            return {"error": "Authorization problem"}, 401
        db.session.delete(order)
        db.session.commit()
        return {"msg": "Success"}, 200
