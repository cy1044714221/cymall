from django.db import transaction
from django_redis import get_redis_connection
from rest_framework import serializers
from django.utils import timezone
from .models import OrderInfo, OrderGoods
from goods.models import SKU


class CreateOrderSerializer(serializers.ModelSerializer):
    """
        下单数据序列化器
        """

    class Meta:
        model = OrderInfo
        fields = ('order_id', 'address', 'pay_method')
        read_only_fields = ('order_id',)
        extra_kwargs = {
            'address': {
                'write_only': True,
                'required': True,
            },
            'pay_method': {
                'write_only': True,
                'required': True
            }
        }

    def create(self, validated_data):
        """保存订单"""
        user = self.context['request'].user
        validated_data['user'] = user
        validated_data['order_id'] = timezone.now().strftime('%Y%m%d%H%M%S') + ('%09d' % validated_data['user'].id)

        # if validated_data['pay_method'] == 1:   # 1为货到付款 订单状态改为待发货
        #     validated_data['order_status'] = 2
        # else:
        #     validated_data['order_status'] = 1

        # 若支付方式为1(货到付款)， 订单状态为2(待发货)，  否则为待支付(1)
        validated_data['order_status'] = (2 if validated_data['pay_method'] == 1 else 1)
        validated_data['total_count'] = 0
        validated_data['total_amount'] = 0

        with transaction.atomic():  # 开启事务
            save_id = transaction.savepoint()  # 创建一个事务回滚保存点
            try:
                orderinfo = OrderInfo.objects.create(**validated_data)

                # 获取购物车信息
                redis_conn = get_redis_connection("cart")
                redis_cart = redis_conn.hgetall("cart_%s" % user.id)
                cart_selected = redis_conn.smembers('cart_selected_%s' % user.id)
                # 将bytes类型转换为int类型
                cart = {}
                try:
                    for sku_id in cart_selected:
                        cart[int(sku_id)] = int(redis_cart[sku_id])
                except:
                    raise serializers.ValidationError('订单不能为空')
                # 处理订单商品
                sku_id_list = cart.keys()
                for sku_id in sku_id_list:
                    while True:
                        sku = SKU.objects.get(id=sku_id)
                        sku_count = cart[sku.id]

                        # 判断库存
                        s = sku.stock
                        if sku_count > sku.stock:  # 原始库存:
                            raise serializers.ValidationError('商品库存不足')

                        # 减少库存
                        # sku.stock -= sku_count
                        # sku.sales += sku_count  # 应该改为支付后修改销量
                        # sku.save()
                        stock = sku.stock - sku_count
                        sales = sku.sales + sku_count
                        result = SKU.objects.filter(stock=sku.stock, id=sku_id).update(stock=stock, sales=sales)
                        if result == 0:
                            continue

                        # 累计商品的SPU 销量信息
                        sku.goods.sales += sku_count  # 应该改为支付后修改销量
                        sku.goods.save()

                        # 累计订单基本信息的数据
                        orderinfo.total_count += sku_count  # 累计总数量
                        orderinfo.total_amount += (sku.price * sku_count)  # 累计总额

                        # 保存订单商品
                        OrderGoods.objects.create(order_id=orderinfo, sku_id=sku, count=sku_count, price=sku.price)
                        break

                orderinfo.save()

            except serializers.ValidationError:
                raise
            except Exception as e:
                #  logger.error(e)
                transaction.savepoint_rollback(save_id)
                raise

            # 提交事务
            transaction.savepoint_commit(save_id)

            # 清空 redis中 勾选的购物车数据
            redis_conn.hdel('cart_%d' % user.id, *cart_selected)
            redis_conn.srem('selected_%d' % user.id, *cart_selected)

        return orderinfo
