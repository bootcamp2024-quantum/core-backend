from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)
  repeat_password = serializers.CharField(write_only=True)

  class Meta:
    model = User
    fields = ('username', 'email', 'password', 'repeat_password')

  def validate(self, attrs):
    password = attrs.get('password')
    repeat_password = attrs.get('repeat_password')
    if password != repeat_password:
      raise serializers.ValidationError('Passwords do not match.')
    return attrs

  def create(self, validated_data):
    user = User.objects.create_user(
        validated_data['username'],
        validated_data['email'],
        validated_data['password']
    )
    user.save()
    return user
