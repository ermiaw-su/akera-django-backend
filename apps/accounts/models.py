from mongoengine import Document, StringField, EmailField, DateTimeField, DateField
import datetime
from django.db import models

# Define Roles
ROLES_CHOICES = [
    ('admin', 'Admin'),
    ('doctor', 'Doctor'),
    ('user', 'User'),
]

# Define Gender
GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
]

# Create your models here.
class User(Document):
    username = StringField(max_length=50, unique=True, required=True)
    email = EmailField(max_length=50, required=True)
    password = StringField(max_length=100, required=True)
    role = StringField(max_length=15, choices=ROLES_CHOICES, default='user')
    create_at = DateTimeField(default=datetime.datetime.now())
    address = StringField()
    birthDate = DateField()
    fullName = StringField()
    gender = StringField(choices=GENDER_CHOICES, default='male')
    phone = StringField()
    
    meta = {'collection': 'users'}