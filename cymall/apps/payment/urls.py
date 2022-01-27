from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [

    # 支付宝支付
    path('payment/<order_id>', views.PaymentStatus.as_view()),  # 支付请求url
    path('payment_status', views.PaymentStatusSaveView.as_view()),  # 支付返回重定向





]