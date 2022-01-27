import logging

from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from alipay import AliPay, DCAliPay, ISVAliPay
from alipay.utils import AliPayConfig

from orders.models import OrderInfo
from .models import Payment


class PaymentStatus(APIView):
    """支付"""
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        user = request.user
        try:
            order = OrderInfo.objects.get(order_id=order_id, user=user, order_status=1)
        except OrderInfo.DoesNotExist:
            return Response({'message': '订单信息有错误'}, status=status.HTTP_400_BAD_REQUEST)

        # 支付宝支付
        alipay = AliPay(
            appid="2021000119604948",
            app_notify_url=None,  # 默认回调 url
            app_private_key_string=open(
                "/Users/phoenix/Desktop/mall/cymall/apps/payment/keys/app_private_key.pem").read(),
            alipay_public_key_string=open(
                "/Users/phoenix/Desktop/mall/cymall/apps/payment/keys/cat app_publict_key.pem").read(),
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True,  # 默认 False
            verbose=False,  # 输出调试数据
            config=AliPayConfig(timeout=15)  # 可选，请求超时时间
        )

        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=str(order.total_amount),
            subject='Cymall%s' % order_id,
            return_url="http://127.0.0.1:8000/payment_status",
            notify_url=""  # 可选，不填则使用默认 notify url
        )
        # 沙箱环境域名， 正式去掉dev   debug= False
        alipay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string
        print(alipay_url)
        return Response({'alipay_url': alipay_url})


#  沙箱环境账号
# 买家账号    rekmki8730@sandbox.com
# 登录密码111111
# 支付密码111111

# 支付宝支付成功返回链接：
# http://127.0.0.1:8000/?charset=utf-8&out_trade_no=20220126120655000000001&method=alipay.trade.page.pay.return&total_amount=33983.00&sign=aa6nC8Lo49ri%2B6LwrhZm4s1VZ%2FbfHS14edNcjFQ9ilzk8spcBv1D8WyV7Y2t3knlOorn1EwQiW9bNopo3GrWOCttDj1ZwX5ZVNjHGHNr2nvCXJ3HeJ%2BBKNH4Or7Erlw6Pnre3WhxdpNepx7hCo%2FTiMI%2FPJWZRhiOYSmJN66ciWZ2s4P7jfbiO0t8G8J96e2AFBsHhckLcgKg5%2BomqgohkU9MAS7JewknpuSViHzX7vBEqQjdEc2%2BUf7XpelqirAvQk%2F3zu1oeI4BsxgbxrNbVDcrw4TtXSd%2FyScgwJVqZ9xqxr1969L56NaV21wE6dso7MX99FgC6MSnSgcV9KMMYw%3D%3D&trade_no=2022012622001469950501650568&auth_app_id=2021000119604948&version=1.0&app_id=2021000119604948&sign_type=RSA2&seller_id=2088621957692526&timestamp=2022-01-26+23%3A42%3A53
# http://127.0.0.1:8000/?
# charset=utf-8
# &out_trade_no=20220126120655000000001
# &method=alipay.trade.page.pay.return
# &total_amount=33983.00
# &sign=aa6nC8Lo49ri%2B6LwrhZm4s1VZ%2FbfHS14edNcjFQ9ilzk8spcBv1D8WyV7Y2t3knlOorn1EwQiW9bNopo3GrWOCttDj1ZwX5ZVNjHGHNr2nvCXJ3HeJ%2BBKNH4Or7Erlw6Pnre3WhxdpNepx7hCo%2FTiMI%2FPJWZRhiOYSmJN66ciWZ2s4P7jfbiO0t8G8J96e2AFBsHhckLcgKg5%2BomqgohkU9MAS7JewknpuSViHzX7vBEqQjdEc2%2BUf7XpelqirAvQk%2F3zu1oeI4BsxgbxrNbVDcrw4TtXSd%2FyScgwJVqZ9xqxr1969L56NaV21wE6dso7MX99FgC6MSnSgcV9KMMYw%3D%3D
# &trade_no=2022012622001469950501650568
# &auth_app_id=2021000119604948
# &version=1.0&app_id=2021000119604948
# &sign_type=RSA2&seller_id=2088621957692526
# &timestamp=2022-01-26+23%3A42%3A53


class PaymentStatusSaveView(APIView):
    """支付结果"""

    def get(self, request):
        data = request.query_params.dict()
        print(data)
        sign = data.pop('sign')

        alipay = AliPay(
            appid="2021000119604948",
            app_notify_url=None,  # 默认回调 url
            app_private_key_string=open(
                "/Users/phoenix/Desktop/mall/cymall/apps/payment/keys/app_private_key.pem").read(),
            alipay_public_key_string=open(
                "/Users/phoenix/Desktop/mall/cymall/apps/payment/keys/cat app_publict_key.pem").read(),
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True,  # 默认 False
            verbose=False,  # 输出调试数据
            config=AliPayConfig(timeout=15)  # 可选，请求超时时间
        )

        success = alipay.verify(data, sign)  # 对返回支付结果校验
        if success:  # 增加订单支付成功信息， 修改订单状态
            order_id = data.get('out_trade_no')  # ?? 这里字典中为啥会取出来元祖 ？？？
            trade_id = data.get('trade_no')
            print(order_id, type(order_id))
            print(trade_id)
            # order = OrderInfo.objects.get(order_id=order_id)
            Payment.objects.create(
                order_id=order_id,
                trade_id=trade_id
            )

            OrderInfo.objects.filter(order_id=order_id, order_status=1).update(order_status=2)
            return Response({'trade_id': trade_id}, status=status.HTTP_201_CREATED)

        else:
            return Response({'message': '非法请求'}, status=status.HTTP_400_BAD_REQUEST)
