import re

from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Address
from .serializers import CreateUserSerializer, UserDetailSerializer, EmailSerializer, AddressSerializer

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
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):  # 重写方法 从前端获取user
        return self.request.user


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


# 用户地址新增 / 修改
class AddressView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, requst):
        """新建用户地址"""
        serializer = AddressSerializer(data=requst.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        """获取用户地址信息"""
        default_address = request.user.default_address
        address = Address.objects.filter(user=request.user.id, is_deleted=False)
        serializer = AddressSerializer(address, many=True)
        data = {
            'user_id': request.user.id,
            'default_address': default_address,
            'addresses': serializer.data
        }
        return Response(data)


class AddressDetailView(UpdateAPIView):
    """
    put:修改地址
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user.id, is_deleted=False)

    serializer_class = AddressSerializer

    def delete(self, request, pk):
        """逻辑删除"""
        address = self.get_object()
        # 进行逻辑删除
        address.is_deleted = True
        address.save()
        return Response(status=status.HTTP_204_NO_CONTENT)