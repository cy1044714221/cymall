from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [

    # 购物车
    path('carts', views.CartsView.as_view()),




]