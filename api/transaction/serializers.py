from rest_framework import serializers
from app import models
from api.person.serializers import PersonSerializer

class TransactionSerializer(serializers.ModelSerializer):
	person = serializers.SerializerMethodField()

	class Meta:
		model = models.Transaction
		fields = "__all__"

	def get_person(self, instance):
		return PersonSerializer(instance.persons).data