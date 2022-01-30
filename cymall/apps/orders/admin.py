from .models import OrderInfo, OrderGoods
from django.contrib import admin


class OrderGoodsInfoStackedInline(admin.TabularInline):
    model = OrderGoods
    extra = 0
    fields = ['sku_id', 'price', 'count']


@admin.register(OrderInfo, )
class OrderInfoAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'address', 'total_count', 'total_amount', 'pay_method', 'order_status')
    readonly_fields = ('order_id', 'user','pay_method','total_count', )
    list_filter = ('pay_method', 'order_status')
    fields = ('order_id', 'user', 'address', 'total_count', 'total_amount', 'pay_method', 'order_status')
    inlines = [OrderGoodsInfoStackedInline]



@admin.register(OrderGoods, )
class OrderGoodsInfoAdmin(admin.ModelAdmin):
    pass
