from rest_framework import serializers
from .models import Doctor
from apps.poli.models import Poli
from apps.accounts.models import User
from django.contrib.auth.hashers import make_password
from bson import ObjectId

class RegisterSerializer(serializers.Serializer):
    poliId = serializers.CharField(required=True)
    doctorName = serializers.CharField(max_length=50, required=True)
    specialization = serializers.CharField(max_length=50, required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        # Take poli id
        poli_id = data.get('poliId')

        # Check Poli
        poli = Poli.objects(id=ObjectId(poli_id)).first()

        if not poli:
            raise serializers.ValidationError("Poli not found")
        
        if Doctor.objects(
            poli=poli,
            doctorName=data['doctorName']
        ).first():
            raise serializers.ValidationError("Doctor name already exists")
        
        return data
    
    def create(self, validated_data):
        # Take password
        password = validated_data.pop('password')

        # Take poli id
        poli_id = validated_data.pop('poliId')

        # Find poli
        poli = Poli.objects(id=ObjectId(poli_id)).first()

        # Create user
        user = User(
            username=validated_data['doctorName'],
            role="doctor"
        )

        user.password = make_password(password)
        user.save()

        # Create doctor
        doctor = Doctor(
            user=user,
            poli=poli,
            doctorName=validated_data['doctorName'],
            specialization=validated_data['specialization']
        )
        doctor.save()

        return doctor

class UpdateSerializer(serializers.Serializer):
    doctorName = serializers.CharField(max_length=50)
    specialization = serializers.CharField(max_length=50)

    def validate(self, data):
        # Take doctor id
        doctor_id = self.context.get('doctor_id')

        if not doctor_id:
            raise serializers.ValidationError("Doctor id is required")

        # Check doctor
        doctor = Doctor.objects(id=ObjectId(doctor_id)).first()

        if not doctor:
            raise serializers.ValidationError("Poli not found")
        
        if Doctor.objects(
            poli=doctor.poli,
            doctorName=data['doctorName'], 
            id__ne=doctor.id
        ).first():
            raise serializers.ValidationError("Doctor name already exists")
        
        return data
    
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance