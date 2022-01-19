from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    # 用户注册
    path('users', views.UserView.as_view()),

    # 获取用户详情
    path('user', views.UserDetailView.as_view()),
]

# router = DefaultRouter()  # 可以处理视图的路由器
# router.register('users', views.UserView)  # 向路由器中注册视图集
# urlpatterns += router.urls  # 将路由器中的所以路由信息追到到django的路由列表中