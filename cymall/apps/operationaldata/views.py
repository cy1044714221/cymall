from django.shortcuts import render
from datetime import timedelta

from django.utils import timezone
from users.models import User
from goods.models import Goods
from orders.models import OrderInfo


def all_data(request):
    """总用户数 / 总商品数 / 总订单数 / """
    user_count = User.objects.count()
    goods_count = Goods.objects.count()
    orders_count = OrderInfo.objects.count()
    today_orders = OrderInfo.objects.filter(create_date__gt=timezone.now().date()).count()
    return render(request, 'operationaldata/stateboard.html', locals())


def today_data(request):
    """
    今日新增用户 / 今日新增订单 / 今日销售额 /
    昨日新增用户 / 昨日新增订单 / 昨日销售额 /
    """
    today = timezone.now().date()  # 今日数据
    user_count = User.objects.filter(date_joined__gt=today).count()
    orders_count = OrderInfo.objects.filter(create_date__gt=today).count()
    goods_count = Goods.objects.filter(create_date__gt=today).count()
    today_orders = OrderInfo.objects.filter(create_date__gt=timezone.now().date()).count()
    return render(request, 'operationaldata/stateboard.html', locals())

    # yesterday = timezone.now().date() + timedelta(days=-1)  # 昨日数据
