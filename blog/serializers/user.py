from rest_framework import serializers

from ..models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Safe here because a User has no password field.
        fields = '__all__'
