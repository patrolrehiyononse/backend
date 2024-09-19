from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'username', 'role', 'sub_unit', 'is_superuser')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user