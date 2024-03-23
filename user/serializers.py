"""Serializers for the user app."""

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)

from .models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer for tokens obtaining process.
    """

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        """
        Validate the provided credentials and returns created token (access token and refresh token)
        with added user_id field.
        """
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"), username=email, password=password
        )

        if user:
            data = super().validate(attrs)
            data["user_id"] = user.id
            return data
        else:
            return {"message": "Invalid credentials", "code": 400}


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    """
    Custom TokenRefreshSerializer to handle token refresh.
    """

    refresh = serializers.CharField(allow_blank=True)

    def validate(self, attrs):
        """
        Validate the token and return the data if it's valid.
        """
        if not attrs.get("refresh"):
            return {"message": "Field 'refresh' may not be blank.", "code": 400}

        try:
            data = super().validate(attrs)
            return data
        except TokenError as e:
            return {"message": str(e), "code": 500}


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    repeat_password = serializers.CharField(write_only=True)
    avatar = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "repeat_password", "avatar")

    def validate(self, attrs):
        password = attrs.get("password")
        repeat_password = attrs.get("repeat_password")
        if password != repeat_password:
            raise serializers.ValidationError("Passwords do not match.")
        attrs.pop("repeat_password", None)
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["email"],
            validated_data["password"],
            username=validated_data["username"],
            avatar=validated_data["avatar"],
        )
        user.save()
        return user
