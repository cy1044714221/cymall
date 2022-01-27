from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CartsSerializer, CartSKUSerializer
from goods.models import SKU


class CartsView(APIView):
    """购物车"""
    """
    user_id, sku_id, count, is_selected
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """加入购物车"""
        serializer = CartsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        sku_id = serializer.validated_data.get('sku_id')
        count = serializer.validated_data.get(('count'))
        is_selected = serializer.validated_data.get('is_selected')

        redis_conn = get_redis_connection('cart')
        pl = redis_conn.pipeline()
        # 记录购物车商品数量
        pl.hincrby('cart_%s' % user.id, sku_id, count)
        # 记录购物车的勾选项
        # 勾选
        if is_selected:
            pl.sadd('cart_selected_%s' % user.id, sku_id)
        pl.execute()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        """查看购物车信息"""
        user = request.user
        # 从redis中取出 用户对应的购物车数据
        redis_conn = get_redis_connection('cart')
        redis_cart = redis_conn.hgetall('cart_%s' % user.id)
        redis_cart_selected = redis_conn.smembers('cart_selected_%s' % user.id)
        cart = {}
        for sku_id, count in redis_cart.items():
            cart[int(sku_id)] = {
                'count': int(count),
                'selected': sku_id in redis_cart_selected
            }
        #  care = {12: {'count': 2, 'selected': True}, ......}

        # 遍历处理购物车数据
        skus = SKU.objects.filter(id__in=cart.keys())
        for sku in skus:
            sku.count = cart[sku.id]['count']
            sku.selected = cart[sku.id]['selected']

        serializer = CartSKUSerializer(skus, many=True)
        return Response(serializer.data)
