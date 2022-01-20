from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [

    # 用户注册
    path('qq/authorization/', views.QQAuthURLView.as_view()),

    # 登陆后到回调处理
    path('qq/user/', views.QQAuthUserView.as_view()),




]