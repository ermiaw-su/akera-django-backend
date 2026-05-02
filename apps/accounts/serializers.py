from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password
from django.conf import settings
from bson import ObjectId

class RegisterSerializers(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    address = serializers.CharField(required=False)
    birthDate = serializers.DateField(required=False)
    fullName = serializers.CharField(required=False)
    gender = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    role = serializers.CharField(required=False)

    def validate(self, data):
        if User.objects(username=data['username']).first():
            raise serializers.ValidationError("Username already exists")
        
        if User.objects(email=data['email']).first():
            raise serializers.ValidationError("Email already exists")
        
        return data
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = User(**validated_data)
        user.save()

        return user
    
class LoginSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UpdateSerializers(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()

    address = serializers.CharField(required=False)
    birthDate = serializers.DateField(required=False)
    fullName = serializers.CharField(required=False)
    gender = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    role = serializers.CharField(required=False)

    def validate(self, data):
        # Take user id
        user_id = self.context.get('user_id')

        # Find user
        user = User.objects(id=ObjectId(user_id)).first()

        if not user:
            raise serializers.ValidationError("User not found")
        
        # Check user esclude ourself
        if User.objects(username=data['username'], id__ne=user.id).first():
            raise serializers.ValidationError("Username already exists")
        
        if User.objects(email=data['email'], id__ne=user.id).first():
            raise serializers.ValidationError("Email already exists")
        
        return data
    
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance