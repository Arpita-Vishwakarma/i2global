from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "user_name", "user_email", "created_on", "last_update"]


from rest_framework import serializers
from .models import User

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["user_name", "user_email", "password"]

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data["user_email"],
            name=validated_data["user_name"],
            password=validated_data["password"]
        )

class SigninSerializer(serializers.Serializer):
    user_email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data["user_email"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid email or password")
        data["user"] = user
        return data
