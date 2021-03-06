from alipay import AliPay
from flask import request
from flask_restful import Resource
from models.trusteeshipOrder import TrusteeshipOrder, db
from config import app_private_key_string, alipay_public_key_string
from datetime import datetime


class AliPayAPI(Resource):
    def __init__(self):
        self.alipay = AliPay(
            appid="2016092000552187",
            app_notify_url="http://www.itsyuekao.com:5000/api/v0/order/alipay",
            app_private_key_string=app_private_key_string,
            alipay_public_key_string=alipay_public_key_string
        )

    def put(self):
        """
        Start the payment
        :return: alipay url or error message
        """
        json = request.get_json()
        try:
            orders = json["ord_num"]
            subject = json["subject"]
            return_url = json["return_url"]
            wap = json["wap"]
        except KeyError:
            return {"error": "Lack necessary argument"}, 406

        price = 0
        for order in orders:
            order = TrusteeshipOrder.query.filter_by(
                ord_num=order, status=0
            ).first()
            if order is None:
                return {"error": f"Order num {order} not found"}, 404
            price += order.price
        
        if wap:
            sig = self.alipay.api_alipay_trade_wap_pay(
                out_trade_no="&".join(orders),
                subject=subject,
                total_amount=price,
                return_url=return_url
            )
        else:
            sig = self.alipay.api_alipay_trade_page_pay(
                out_trade_no="&".join(orders),
                subject=subject,
                total_amount=price,
                return_url=return_url
            )
        return {
            "alipay_url": "https://openapi.alipaydev.com/gateway.do?" + sig
        }, 200

    @staticmethod
    def post():
        out_trade_no = request.form["out_trade_no"]
        orders = out_trade_no.split("&")
        for ord_num in orders:
            order = TrusteeshipOrder.query.filter_by(
                ord_num=ord_num, status=0
            ).first()
            order.status = 1
            order.open_time = datetime.now()
            db.session.commit()
