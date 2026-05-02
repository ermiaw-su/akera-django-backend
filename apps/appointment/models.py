from mongoengine import Document, StringField, EmailField, DateTimeField, DateField
import datetime
from django.db import models

# Define status
STATUS_CHOICES = [
    ('scheduled', 'Scheduled'),
    ('finished', 'Finished'),
]

# Create your models here.
class Appointment(Document):
    userId = StringField(required=True)
    username = StringField(max_length=50)
    hospitalId = StringField(required=True)
    hospitalName = StringField(max_length=50)
    poliId = StringField(required=True)
    poliName = StringField(max_length=50)
    doctorId = StringField(required=True)
    doctorName = StringField(max_length=50)
    date = DateField(required=True)
    time = StringField(required=True)
    reason = StringField(required=True)
    status = StringField(required=True, choices=STATUS_CHOICES, default='scheduled')
    create_at = DateTimeField(default=datetime.datetime.now())