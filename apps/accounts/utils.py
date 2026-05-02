import jwt
import datetime
from django.conf import settings

def generate_jwt(user):
    payload = {
        "user_id": str(user.id),
        "username": user.username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        "iat": datetime.datetime.utcnow()
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")