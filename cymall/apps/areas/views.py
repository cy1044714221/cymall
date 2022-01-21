from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework_extensions.cache.mixins import ListCacheResponseMixin

from .serializers import SubsAreasSerializer, AreasSerializer
from .models import Area


class AreasView(ListCacheResponseMixin, ListAPIView):
    """获取顶级地区"""
    serializer_class = AreasSerializer
    queryset = Area.objects.filter(parent=None)


class SubsAreasView(APIView):
    """获取子级地区"""
    serializer_class = SubsAreasSerializer
    queryset = Area.objects.all()

    # @cache_response(timeout=60, cache='areas')  # 缓存
    def get(self, request, pk):
        try:
            area = Area.objects.get(id=pk)
        except Area.DoesNotExist:
            return Response({'message':'地址字段错误'}, status=status.HTTP_400_BAD_REQUEST)
        serializers = SubsAreasSerializer(area)
        return Response(serializers.data)

