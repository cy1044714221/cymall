from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import User


def jwt_response_payload_handler(token, user=None, request=None):
    """重写JWT登陆视图，增加返回值"""
    return {
        'user_id': user.id,
        'username': user.username,
        "mobile": user.mobile,
        "email": user.email,
        "email_active": user.email_active,
        'token': token,
    }


# 多账号方式登录
class MultiAccountAuth(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):

        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
        except User.DoesNotExist:
            return None

        if user is not None and user.check_password(password):
            return user
