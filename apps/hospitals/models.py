from mongoengine import Document, StringField, EmailField, DateTimeField, DateField
import datetime
from django.db import models

# Create your models here.
class Hospital(Document):
    hospitalName = StringField(max_length=100, required=True)
    address = StringField(max_length=100, required=True)
    phone = StringField(max_length=15, required=True)
    create_at = DateTimeField(default=datetime.datetime.now())

    meta = {'collection': 'hospitals'}