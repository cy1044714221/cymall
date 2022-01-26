from .models import OrderInfo
from django.contrib import admin


@admin.register(OrderInfo, )
class OrderInfoAdmin(admin.ModelAdmin):
    pass
