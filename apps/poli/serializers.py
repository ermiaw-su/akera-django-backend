from rest_framework import serializers
from .models import Poli
from apps.hospitals.models import Hospital
from django.contrib.auth.hashers import make_password
from django.conf import settings
from bson import ObjectId

class RegisterSerializer(serializers.Serializer):
    hospitalId = serializers.CharField(required=True)
    poliName = serializers.CharField(max_length=50, required=True)
    poliCode = serializers.CharField(max_length=50, required=True)

    def validate(self, data):
        # Take hospital id
        hospital_id = data.get('hospitalId')

        hospital = Hospital.objects(id=ObjectId(hospital_id)).first()
        
        if not hospital:
            raise serializers.ValidationError("Hospital not found")
        
        if Poli.objects(
            hospital=hospital,
            poliName=data['poliName']
        ).first():
            raise serializers.ValidationError("Poli name already exists")
        
        return data

    def create(self, validated_data):
        # Take hospital id
        hospital_id = validated_data.pop('hospitalId')

        # Find hospital
        hospital = Hospital.objects(id=ObjectId(hospital_id)).first()

        # Create poli
        poli = Poli(
            hospital=hospital,
            **validated_data
        )
        poli.save()

        return poli
    
class UpdateSerializer(serializers.Serializer):
    poliName = serializers.CharField(max_length=50)
    poliCode = serializers.CharField(max_length=50)

    def validate(self, data):
        poli_id = self.context.get('poli_id')

        if not poli_id:
            raise serializers.ValidationError("Poli id is required")
        
        poli = Poli.objects(id=ObjectId(poli_id)).first()

        if not poli:
            raise serializers.ValidationError("Poli is not found")
        
        if Poli.objects(poliName=data['poliName'], id__ne=poli.id).first():
            raise serializers.ValidationError("Poli name already exists")
        
        return data

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance