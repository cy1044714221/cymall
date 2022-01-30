from .models import OrderInfo, OrderGoods
from django.contrib import admin


@admin.register(OrderInfo, )
class OrderInfoAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'address', 'total_count', 'total_amount', 'pay_method', 'order_status')
    list_filter = ('pay_method', 'order_status')
    

@admin.register(OrderGoods, )
class OrderGoodsInfoAdmin(admin.ModelAdmin):
    pass
