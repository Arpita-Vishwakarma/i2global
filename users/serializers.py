from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'user_name', 'user_email', 'created_on']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['user_name', 'user_email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data['user_email'],
            name=validated_data['user_name'],
            password=validated_data['password']
        )
