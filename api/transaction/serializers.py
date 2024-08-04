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

class PathTraceSerializer(serializers.ModelSerializer):
	person = serializers.SerializerMethodField()

	class Meta:
		model = models.PathTrace
		fields = ['id', 'lat', 'lng', 'person']

	def get_person(self, instance):
		return PersonSerializer(instance.persons).data

class DeployedUnitPersonSerializer(serializers.ModelSerializer):
	person_id = serializers.IntegerField()
	person = serializers.SerializerMethodField()

	class Meta:
		model = models.DeployedUnitPerson
		fields = ['person_id', 'person', 'is_arrived']
	def get_person(self, obj):
		return {
			"full_name": obj.person.full_name,
			"rank": obj.person.person_rank.description,
			"unit": obj.person.person_unit.description,
			"station": obj.person.person_station.description
		}
class DeployedUnitsSerializer(serializers.ModelSerializer):
	persons = DeployedUnitPersonSerializer(many=True, write_only=True)
	persons_read = DeployedUnitPersonSerializer(
		source='deployedunitperson_set', many=True, read_only=True)

	class Meta:
		model = models.DeployedUnits
		fields = ['id', 'destination', 'coordinates', 'deployment_name', 'is_done',
				  'persons', 'persons_read']

	def create(self, validated_data):
		persons_data = validated_data.pop('persons')
		deployed_unit = models.DeployedUnits.objects.create(**validated_data)
		for person_data in persons_data:
			print(person_data)
			models.DeployedUnitPerson.objects.create(
                deployed_unit=deployed_unit,
                person_id=person_data['person_id'],
                is_arrived=person_data.get('is_arrived', False)
            )
		return deployed_unit

	def update(self, instance, validated_data):
		persons_data = validated_data.pop('persons')
		instance.destination = validated_data.get('destination', instance.destination)
		instance.coordinates = validated_data.get('coordinates', instance.coordinates)
		instance.deployment_name = validated_data.get('deployment_name', instance.deployment_name)
		instance.save()

		for person_data in persons_data:
			deployed_unit_person, created = models.DeployedUnitPerson.objects.get_or_create(
                deployed_unit=instance,
                person_id=person_data['person_id'],
            )
			deployed_unit_person.is_arrived = person_data.get('is_arrived', deployed_unit_person.is_arrived)
			deployed_unit_person.save()
		return instance
