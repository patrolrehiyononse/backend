from rest_framework import serializers
from app import models


class GeofencingSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Geofencing
        fields = '__all__'