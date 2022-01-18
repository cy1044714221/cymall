from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, GenericAPIView

from .models import User
from .serializers import UserSerializer


class UserView(CreateAPIView):
    """
    post:新增用户
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()


