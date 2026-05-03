from rest_framework import serializers
from .models import Appointment
from .models import Diagnoses
from .models import Medicines
from apps.accounts.models import User
from apps.hospitals.models import Hospital
from apps.poli.models import Poli
from apps.doctors.models import Doctor
from django.conf import settings
from bson import ObjectId

class BookSerializer(serializers.Serializer):
    hospitalId = serializers.CharField(required=True)
    poliId = serializers.CharField(required=True)
    doctorId = serializers.CharField(required=True)
    date = serializers.DateField(required=True)
    time = serializers.TimeField(required=True)
    reason = serializers.CharField(required=True)

    def validate(self, data):
        # Take user
        user = self.context.get('user')

        if not user:
            raise serializers.ValidationError("User not found")
        
        # One day only 2 appointments
        booking_count = Appointment.objects(
            user=user,
            date=data['date']
        ).count()

        if booking_count >= 2:
            raise serializers.ValidationError("You can only book 2 appointments per day")
        
        # Take hospital id
        hospital_id = data.get('hospitalId')

        if not hospital_id:
            raise serializers.ValidationError("Hospital id is required")

        hospital = Hospital.objects(id=ObjectId(hospital_id)).first()

        if not hospital:
            raise serializers.ValidationError("Hospital not found")
        
        # Take poli id
        poli_id = data.get('poliId')

        if not poli_id:
            raise serializers.ValidationError("Poli id is required")

        poli = Poli.objects(id=ObjectId(poli_id)).first()

        if not poli:
            raise serializers.ValidationError("Poli not found")
        
        if poli.hospital.id != hospital.id:
            raise serializers.ValidationError("Poli not belong to this hospital")
        
        # Take doctor id
        doctor_id = data.get('doctorId')

        if not doctor_id:
            raise serializers.ValidationError("Doctor id is required")

        doctor = Doctor.objects(id=ObjectId(doctor_id)).first()

        if not doctor:
            raise serializers.ValidationError("Doctor not found")
        
        if doctor.poli.id != poli.id:
            raise serializers.ValidationError("Doctor not belong to this poli")
        
        return data
    
    def create(self, validated_data):
        # Take user from context
        user = self.context.get('user')

        # Take hospital id
        hospital_id = validated_data.pop('hospitalId')

        # Take poli id
        poli_id = validated_data.pop('poliId')

        # Take doctor id
        doctor_id = validated_data.pop('doctorId')

        # Find hospital
        hospital = Hospital.objects(id=ObjectId(hospital_id)).first()

        # Find poli
        poli = Poli.objects(id=ObjectId(poli_id)).first()

        # Find doctor
        doctor = Doctor.objects(id=ObjectId(doctor_id)).first()

        time_value = validated_data.pop('time')

        # Create appointment
        appointment = Appointment(
            user=user, 
            hospital=hospital, 
            poli=poli, 
            doctor=doctor,
            time=str(time_value),
            **validated_data
        )
        appointment.save()

        return appointment
    
class CancelSerializer(serializers.Serializer):

    def validate(self, data):
        # Take appointment id
        appointment_id = self.context.get('id')

        # Find appointment
        appointment = Appointment.objects(id=ObjectId(appointment_id)).first()

        if not appointment:
            raise serializers.ValidationError("Appointment not found")
        
        if appointment.status != 'scheduled':
            raise serializers.ValidationError("You can only cancel scheduled appointments")
        
        self.context['appointment'] = appointment
        
        return data
    
    def save(self):
        # Take appointment
        appointment = self.context.get('appointment')

        appointment.status = 'canceled'
        appointment.save()

        return appointment
    
class GetSerializer(serializers.Serializer):
    id = serializers.CharField()
    status = serializers.CharField()
    date = serializers.DateField()
    time = serializers.CharField()
    reason = serializers.CharField()

    hospitalName = serializers.CharField(source='hospital.hospitalName')
    poliName = serializers.CharField(source='poli.poliName')
    doctorName = serializers.CharField(source='doctor.doctorName')

class MedicineSerializer(serializers.Serializer):
    medicine = serializers.CharField(max_length=100)
    dosage = serializers.CharField(max_length=100)

class DiagnosisSerializer(serializers.Serializer):
    description = serializers.CharField()
    medicines = MedicineSerializer(many=True)

    def validate(self, data):
        # Take appointment
        appointment = self.context.get('appointment')

        if not appointment:
            raise serializers.ValidationError("Appointment not found")
        
        # Check if medicine already exist
        if Diagnoses.objects(appointment=appointment).first():
            raise serializers.ValidationError("Diagnoses already exists")
        
        medicines = data.get('medicines', [])

        if not medicines:
            raise serializers.ValidationError("Medicines is required")
        
        medicine_names = [m['medicine'] for m in medicines]
        if len(medicine_names) != len(set(medicine_names)):
            raise serializers.ValidationError("Duplicate medicines in request")
        
        return data
    
    def create(self, validated_data):
        # Take appointment
        appointment = self.context.get('appointment')

        # Take medicines
        medicines_data = validated_data.pop('medicines')

        # create diagnoses
        diagnosis = Diagnoses(
            appointment=appointment,
            **validated_data
        )
        diagnosis.save()

        # create medicines
        for med in medicines_data:
            medicine = Medicines(
                diagnosis=diagnosis,
                medicine=med['medicine'],
                dosage=med['dosage']
            ).save()
        return diagnosis