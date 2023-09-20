from rest_framework import serializers
from app import models

class RankSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Rank
		fields = "__all__"