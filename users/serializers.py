from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'phone_number', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class CustomUserDetailSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=settings.MAX_USERNAME_LENGTH)

    def validate(self, data):
        print('in validate:', data)
        try:
            user_obj = CustomUser.objects.get(username=data['username'])
            print(f'in validate | user_obj: {user_obj}')
        except:
            serializers.ValidationError("Incorrect username")
        return data


class TestUser(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'phone_number')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")
