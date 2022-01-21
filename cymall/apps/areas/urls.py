from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [

    # 顶底地址
    path('areas', views.AreasView.as_view()),
    # 子级地址
    path('areas/<pk>', views.SubsAreasView.as_view()),




]