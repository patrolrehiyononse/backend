from rest_framework import serializers
from app import models
from api.unit.serializers import SubUnitSerializer

class StationSerializer(serializers.ModelSerializer):
	sub_unit = serializers.SerializerMethodField()

	class Meta:
		model = models.Station
		fields = "__all__"

	def get_sub_unit(self, instance):
		return SubUnitSerializer(instance.sub_unit).data

# class SubStationSerializer(serializers.ModelSerializer):

# 	class Meta:
# 		model = models.SubStation
# 		fields = "__all__"