from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

from .serializers import CreateOrderSerializer
# Create your views here.
from rest_framework.generics import CreateAPIView


class CreateOrderView(CreateAPIView):
    serializer_class = CreateOrderSerializer
    permission_classes = [IsAuthenticated]

