from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from .serializers import UpdateSerializer
from django.contrib.auth.hashers import check_password
from .models import Hospital
from apps.accounts.models import User
from bson import ObjectId
import jwt
from django.conf import settings

# Create your views here.
class RegisterView(APIView):
    def get_admin(self, request):
        # Get token
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None

        try:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")

            user = User.objects(id=ObjectId(user_id)).first()

            # Check if user is admin
            if not user or user.role != 'admin':
                return None

            return user
        except Exception as e:
            print(e)
            return None
        
    def post(self, request):
        # Get admin
        admin = self.get_admin(request)

        if not admin:
            return Response({
                "error": "Admin access is required"
            }, status=403)
        
        # Take data
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        # Create hospital
        hospital = serializer.save()

        # Response
        return Response({
            "id": str(hospital.id),
            "hospitalName": hospital.hospitalName
        }, status=status.HTTP_201_CREATED)
    
class UpdateView(APIView):
    def get_admin(self, request):
        # Get token
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None

        try:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")

            user = User.objects(id=ObjectId(user_id)).first()

            # Check if user is admin
            if not user or user.role != 'admin':
                return None

            return user
        except Exception as e:
            print(e)
            return None
        
    def put(self, request, id):
        # Get admin
        admin = self.get_admin(request)

        if not admin:
            return Response({
                "error": "Admin access is required"
            }, status=403)
        
        # Find hospital
        hospital = Hospital.objects(id=ObjectId(id)).first()

        if not hospital:
            return Response({
                "error": "Hospital not found"
            }, status=404)
        
        # Take data
        serializer = UpdateSerializer(
            instance=hospital,
            data=request.data,
            context={"hospital_id": str(id)}
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        # Update hospital
        hospital = serializer.save()

        # Response
        return Response({
            "id": str(hospital.id),
            "hospitalName": hospital.hospitalName
        }, status=status.HTTP_200_OK)