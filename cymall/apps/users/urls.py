from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    # 注册用户名是否已经存在
    # re_path(r'usernames/(?P<username>\w{5,20})/count', views.UsernameCountView.as_view()),
    path('usernames/<username>/count', views.UsernameCountView.as_view()),

    # 用户注册
    path('users', views.UserView.as_view()),

    # 用户详情
    path('user', views.UserDetailView.as_view()),

    # 修改/验证 邮箱
    path('email', views.EmaillView.as_view()),

    # 验证邮箱
    path('email_verify_url', views.EmailVerifylView.as_view()),


]