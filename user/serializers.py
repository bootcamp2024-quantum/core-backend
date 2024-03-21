"""Serializers for the user app."""
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), username=email, password=password)

        if user:
            data = super().validate(attrs)
            data['user_id'] = user.id
            return data
        else:
            return {"message": "Invalid credentials", "code": 400}
