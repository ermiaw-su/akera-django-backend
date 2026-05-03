from mongoengine import Document, StringField, EmailField, DateTimeField, DateField, ReferenceField
import datetime
from django.db import models

# Define status
STATUS_CHOICES = [
    ('scheduled', 'Scheduled'),
    ('finished', 'Finished'),
    ('canceled', 'Canceled'),
]

# Create your models here.
class Appointment(Document):
    user = ReferenceField('User', required=True)
    hospital = ReferenceField('Hospital', required=True)
    poli = ReferenceField('Poli', required=True)
    doctor = ReferenceField('Doctor', required=True)
    
    date = DateField(required=True)
    time = StringField(required=True)
    reason = StringField(required=True)
    status = StringField(required=True, choices=STATUS_CHOICES, default='scheduled')
    create_at = DateTimeField(default=datetime.datetime.now())

    meta = {'collection': 'appointments'}

class Diagnoses(Document):
    appointment = ReferenceField(Appointment, required=True)
    description = StringField(required=True)
    create_at = DateTimeField(default=datetime.datetime.now())
    meta = {'collection': 'diagnoses'}

class Medicines(Document):
    diagnosis = ReferenceField(Diagnoses, required=True)
    medicine = StringField(required=True)
    dosage = StringField(required=True)
    create_at = DateTimeField(default=datetime.datetime.now())
    meta = {'collection': 'medicines'}