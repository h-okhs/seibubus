# coding: utf-8
from rest_framework import serializers
from ws.models import BusStatus


class BusStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusStatus
        fields = ('line', 'departureAt')
