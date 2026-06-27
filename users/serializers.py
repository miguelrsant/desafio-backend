from rest_framework import serializers

from .models import User


class CreateUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=6,
    )

    class Meta:
        model = User
        fields = [
            "username",
            "password",
        ]


class LoginUserSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
