from rest_framework import serializers
from app import models

class StationSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.Station
		fields = "__all__"

# class SubStationSerializer(serializers.ModelSerializer):

# 	class Meta:
# 		model = models.SubStation
# 		fields = "__all__"