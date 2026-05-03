from mongoengine import Document, StringField, DateTimeField, DateField, ReferenceField
import datetime
from django.db import models
from apps.appointment.models import Appointment

# Create your models here.
class Diagnoses(Document):
    appointment = ReferenceField(Appointment, required=True)
    description = StringField(required=True)
    create_at = DateTimeField(default=datetime.datetime.now())
    meta = {'collection': 'diagnoses'}