from .models import Area

from rest_framework import serializers


class AreasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id', 'name']


class SubsAreasSerializer(serializers.ModelSerializer):
    subs = AreasSerializer(read_only=True, many=True)

    class Meta:
        model = Area
        fields = ['id', 'name', 'subs']
