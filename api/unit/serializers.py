from rest_framework import serializers
from app import models
import logging



class UnitSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Unit
        fields = "__all__"



class SubUnitSerializer(serializers.ModelSerializer):
    unit = serializers.SerializerMethodField()
    class Meta:
        model = models.SubUnit
        fields = "__all__"

    def get_unit(self, instance):
        return UnitSerializer(instance.units).data