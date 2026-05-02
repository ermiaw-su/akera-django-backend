from rest_framework import serializers
from .models import Hospital
from django.contrib.auth.hashers import make_password
from django.conf import settings
from bson import ObjectId

class RegisterSerializer(serializers.Serializer):
    hospitalName = serializers.CharField()
    address = serializers.CharField()
    phone = serializers.CharField()

    def validate(self, data):
        if Hospital.objects(hospitalName=data['hospitalName']).first():
            raise serializers.ValidationError("Hospital name already exists")
        
        return data
    
    def create(self, validated_data):
        hospital = Hospital(**validated_data)
        hospital.save()

        return hospital
    
class UpdateSerializer(serializers.Serializer):
    hospitalName = serializers.CharField()
    address = serializers.CharField()
    phone = serializers.CharField()

    def validate(self, data):
        hospital_id = self.context.get('hospital_id')

        if not hospital_id:
            raise serializers.ValidationError("Hospital id is required")

        hospital = Hospital.objects(id=ObjectId(hospital_id)).first()

        if not hospital:
            raise serializers.ValidationError("Hospital not found")
        
        if Hospital.objects(hospitalName=data['hospitalName'], id__ne=hospital.id).first():
            raise serializers.ValidationError("Hospital name already exists")
        
        return data
    
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance