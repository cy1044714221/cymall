from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, GenericAPIView

from .models import User
from .serializers import UserSerializer, UserDetailSerializer


class UserView(CreateAPIView):
    """
    post:新增用户
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    #
    # def get_serializer_class(self):
    #     if self.action == "create":
    #         return UserSerializer
    #     return UserDetailSerializer
    #
    # def get_object(self):
    #     """重写此方法的返回值，返回要展示的用户模型对象"""
    #     return self.request.user


class UserDetailView(RetrieveAPIView):
    """
    get: 获取用户信息
    """
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]  # 指定权限 必须登陆用户才能获取到自己的信息

    def get_object(self):
        return self.request.user  # 重写此方法的返回值，返回要展示的用户模型对象
