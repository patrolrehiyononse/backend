from rest_framework import serializers
from app import models


class UnitSerializer(serializers.ModelSerializer):
    sub_unit = serializers.SerializerMethodField()

    class Meta:
        model = models.Unit
        fields = "__all__"

    # 	unit_code = models.CharField(max_length=255, null=True, blank=True)
    # description = models.CharField(max_length=255, null=True, blank=True)

    def get_sub_unit(self, instance):
        obj = models.SubUnit.objects.filter(units=instance)
        return SubUnitSerializer(obj, many=True).data


class SubUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SubUnit
        fields = "__all__"