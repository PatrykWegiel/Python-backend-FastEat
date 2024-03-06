from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(read_only=True)
    image = serializers.ImageField(read_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        username = data.get("email")
        password = data.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )
            if not user:
                msg = "Unable to log in with provided credentials."
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code="authorization")

        data["user"] = user
        return data


class UserPasswordChangeSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(required=True, allow_blank=False)

    class Meta:
        model = User
        fields = ["password", "new_password"]


class UserImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        max_length=None, allow_empty_file=True, allow_null=True, required=False
    )

    class Meta:
        model = User
        fields = ["image"]
