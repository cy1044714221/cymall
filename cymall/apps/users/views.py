import re

from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import CreateUserSerializer, UserDetailSerializer, EmailSerializer

from cymall.utils.signature import Signature


class UsernameCountView(APIView):
    """用户名是否已经存在"""

    def get(self, request, username):
        if not re.match(r'\w{5,20}', username):
            return Response({'username': username, "message": "用户名不合法,请输入5-20位字符"},
                            status=status.HTTP_400_BAD_REQUEST)
        count = User.objects.filter(username=username).count()
        data = {'username': username, 'count': count}
        return Response(data)


class UserView(CreateAPIView):
    """用户注册"""
    serializer_class = CreateUserSerializer


class UserDetailView(RetrieveAPIView):
    """用户详情"""
    def get_object(self):  # 重写方法 从前端获取user
        return self.request.user

    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]


class EmaillView(UpdateAPIView):
    """更新邮箱"""
    def get_object(self):  # 重写方法 从前端获取user
        return self.request.user

    serializer_class = EmailSerializer
    permission_classes = [IsAuthenticated]


class EmailVerifylView(APIView):
    """验证邮箱"""
    def get(self, request):
        token = request.query_params.get('token')
        if not token:
            return Response({'message': 'token无效'}, status=status.HTTP_400_BAD_REQUEST)
        data = Signature(300).decryption_fields(token=token)
        if data is None:
            return Response({'message': '链接信息无效'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                user = User.objects.get(**data)
            except User.DoesNotExist:
                return Response({'message': '用户信息不正确'})
            user.email_active = True
            user.save()
            return Response({'message': 'OK'})
