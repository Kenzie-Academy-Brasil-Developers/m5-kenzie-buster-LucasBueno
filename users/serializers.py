from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
import ipdb


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=127)
    password = serializers.CharField(max_length=100, write_only=True)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    birthdate = serializers.DateField(allow_null=True, default=None)
    is_employee = serializers.BooleanField(allow_null=True, default=False)
    is_superuser = serializers.BooleanField(read_only=True)

    def validate_email(self, value):
        valid = User.objects.filter(
            email__iexact=value
        ).first()
        if valid:
            raise serializers.ValidationError("email already registered.")
        return value

    def validate_username(self, value):
        username = User.objects.filter(
            username__iexact=value
        ).first()
        if username:
            raise serializers.ValidationError("username already taken.")
        return value

    def create(self, validated_data: dict):
        if validated_data["is_employee"]:
            employee = User.objects.create_superuser(**validated_data)
            return employee
        user = User.objects.create_user(**validated_data)

        return user
    
    def update(self, instance: User, validated_data: dict):
        password = validated_data['password']
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, write_only=True)
    password = serializers.CharField(max_length=100, write_only=True)