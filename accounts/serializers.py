from rest_framework import serializers
from accounts.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import authenticate



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

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
    

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    def create(self, validated_data):
        return super().create(validated_data)

    def save(self, **kwargs):
        token=RefreshToken(self.validated_data['refresh'])
        token.blacklist()
        

class CustomLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        data['user'] = user
        return data
    
class CustomRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, data):
        refresh_token = data["refresh"]

       
        refresh = RefreshToken(refresh_token)
        new_access_token = refresh.access_token

        return {
                "access": str(new_access_token)
            }
    


        

    
