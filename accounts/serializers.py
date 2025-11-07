from rest_framework import serializers
from accounts.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(required=True) 

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'phone_number']

    def validate(self, data):
        
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        user = User.objects.create_user( 
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number')
        )
        return user



class CustomLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data['email']
        password = data['password']
        
        
        user = User.objects.get(email=email)
        
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid credentials")

        data['user'] = user
        return data
    
    
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class CustomRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()
