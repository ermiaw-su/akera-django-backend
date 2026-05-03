from mongoengine import Document, StringField, DateTimeField, DateField, ReferenceField
import datetime
from django.db import models
from apps.poli.models import Poli
from apps.accounts.models import User

# Create your models here.
class Doctor(Document):
    user = ReferenceField(User, required=True)
    poli = ReferenceField(Poli, required=True)
    doctorName = StringField(max_length=50, required=True)
    specialization = StringField(max_length=50, required=True)
    create_at = DateTimeField(default=datetime.datetime.now())

    meta = {'collection': 'doctors'}