from django.db import models
from goods.models import BaseModel
from users.models import User, Address
from goods.models import SKU


class OrderInfo(BaseModel):
    """订单"""
    # 订单编号 下单用户id 收货地址 商品总数 订单总金额 付款方式 订单状态
    PAY_METHOD_CHOICES = (
        (1, '货到付款'),
        (2, '支付宝支付'),
    )

    ORDER_STATUS_CHOICES = (
        (1, '待支付'),
        (2, '待发货'),
        (3, '待收货'),
        (4, '待评价'),
        (5, '已完成'),
        (6, '已取消'),
    )
    order_id = models.CharField(max_length=64, primary_key=True, verbose_name='订单号')
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='订单所属用户')
    address = models.ForeignKey(Address, on_delete=models.PROTECT, verbose_name='收获地址')
    total_count = models.IntegerField(default=1, verbose_name='商品总数')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='商品总金额')
    pay_method = models.SmallIntegerField(choices=PAY_METHOD_CHOICES, default=1, verbose_name='支付方式')
    order_status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES, default=1, verbose_name='订单状态')

    class Meta:
        db_table = 'cy_order_info'
        verbose_name = '订单基本信息'
        verbose_name_plural = verbose_name


class OrderGoods(BaseModel):
    """订单商品信息"""
    # 所属订单 商品sku  数量 单价
    order_id = models.ForeignKey('OrderInfo', on_delete=models.CASCADE, verbose_name='订单编号')
    sku_id = models.ForeignKey(SKU, on_delete=models.PROTECT, verbose_name='订单商品SKU')
    count = models.IntegerField(default=1, verbose_name='数量')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='单价')

    class Meta:
        db_table = 'cy_order_goods'
        verbose_name = '订单商品'
        verbose_name_plural = verbose_name


