from mongoengine import Document, StringField, DateTimeField, DateField, ReferenceField
import datetime
from django.db import models
from apps.hospitals.models import Hospital

# Create your models here.
class Poli(Document):
    hospital = ReferenceField(Hospital, required=True)
    poliName = StringField(max_length=50, required=True)
    poliCode = StringField(max_length=50, required=True)
    create_at = DateTimeField(default=datetime.datetime.now())

    meta = {'collection': 'poli'}