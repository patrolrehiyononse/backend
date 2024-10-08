from rest_framework import serializers
from app import models
from api.rank.serializers import RankSerializer
from api.unit.serializers import UnitSerializer
from api.station.serializers import StationSerializer
from api.station.serializers import SubUnitSerializer

class PersonSerializer(serializers.ModelSerializer):
	rank = serializers.SerializerMethodField()
	unit = serializers.SerializerMethodField()
	station = serializers.SerializerMethodField()
	sub_unit = serializers.SerializerMethodField()

	class Meta:
		model = models.Person
		fields = ['id', 'full_name', 'email', 'rank', 'unit', 'station',
				  'person_unit', 'person_rank', 'person_station', 'person_sub_unit',
				  'sub_unit']

	def get_rank(self, instance):
		return RankSerializer(instance.person_rank).data

	def get_unit(self, instance):
		return UnitSerializer(instance.person_unit).data

	def get_station(self, instance):
		return StationSerializer(instance.person_station).data

	def get_sub_unit(self, instance):
		return SubUnitSerializer(instance.person_sub_unit).data