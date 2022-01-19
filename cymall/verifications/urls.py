from django.urls import path, re_path
from .import views


urlpatterns = [
    re_path(r'sms_cods/(?P<phone_num>1[3-9]\d{9})$', views.SendSmsCode.as_view(), name='send_sms_codes')
]