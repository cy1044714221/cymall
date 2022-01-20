from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    # 短信验证码
    re_path(r'sms_codes/(?P<mobile>1[3-9]\d{9})', views.SMSCodeView.as_view()),
]