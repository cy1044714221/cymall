from .models import OrderInfo, OrderGoods
from django.contrib import admin


@admin.register(OrderInfo, )
class OrderInfoAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderGoods, )
class OrderGoodsInfoAdmin(admin.ModelAdmin):
    pass
