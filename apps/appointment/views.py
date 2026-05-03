from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BookSerializer
from .serializers import CancelSerializer
from .serializers import GetSerializer
from .serializers import MedicineSerializer
from .serializers import DiagnosisSerializer
from django.contrib.auth.hashers import check_password
from apps.poli.models import Poli
from apps.accounts.models import User
from apps.hospitals.models import Hospital
from apps.appointment.models import Appointment
from apps.doctors.models import Doctor
from .models import Appointment
from bson import ObjectId
from bson.errors import InvalidId
import jwt
from django.conf import settings

# Create your views here.
class BookView(APIView):
    def get_user(self, request):
        # Get token
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None

        try:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")

            user = User.objects(id=ObjectId(user_id)).first()

            # Check if user is user
            if not user or user.role != 'user':
                return None

            return user
        except Exception as e:
            print(e)
            return None
        
    def post(self, request):
        # Get user
        user =self.get_user(request)

        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Take data
        serializer = BookSerializer(data=request.data, context={"user": user})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Create appointment
        appointment = serializer.save()

        # Response
        return Response({
            "id": str(appointment.id),
            "poliName": appointment.poli.poliName,
            "doctorName": appointment.doctor.doctorName,
            "date": appointment.date,
            "time": appointment.time,
            "status": appointment.status,
        }, status=status.HTTP_201_CREATED)
    
class CancelView(APIView):
    def get_user(self, request):
        # Get token
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None

        try:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")

            user = User.objects(id=ObjectId(user_id)).first()

            # Check if user is user
            if not user or user.role != 'user':
                return None

            return user
        except Exception as e:
            print(e)
            return None
        
    def put(self, request, id):
        # Get user
        user =self.get_user(request)

        # Get appointment
        appointment = Appointment.objects(id=ObjectId(id)).first()

        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if appointment.user.id != user.id:
            return Response({"error": "You are not authorized to cancel this appointment"}, status=status.HTTP_403_FORBIDDEN)
        
        if appointment.user.id != user.id:
            return Response({"error": "Forbidden"}, status=403)
        
        # Take data
        serializer = CancelSerializer(
            data={},
            context={"user": user, "id": id}
        )

        serializer.is_valid(raise_exception=True)
        
        # Cancel appointment
        serializer.save()

        # Response
        return Response({"message": "Appointment canceled"}, status=status.HTTP_200_OK)
    
class GetView(APIView):
    def get_user(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        try:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")

            return User.objects(id=ObjectId(user_id)).first()

        except:
            return None
        
    def get(self, request, id):
        # Get user
        user = self.get_user(request)

        if not user:
            return Response({"error": "Unauthorized"}, status=status.HTTP_404_NOT_FOUND)
        
        # Find appointment
        appointment = Appointment.objects(id=ObjectId(id)).first()

        if not appointment:
            return Response({
                "error": "Appointment not found"
            }, status=404)
        
        if appointment.user.id != user.id:
            return Response({
                "error": "You are not authorized to view this appointment"
            }, status=403)
        
        # Take data
        serializer = GetSerializer(appointment)

        # Response
        return Response(serializer.data, status=200)
    
class HandleView(APIView):
    def get_doctor(self, request):
        # Get token
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None

        try:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")

            user = User.objects(id=ObjectId(user_id)).first()

            # Check if user is user
            if not user or user.role != 'doctor':
                return None
            
            doctor = Doctor.objects(user=user).first()

            return doctor
        except Exception as e:
            print(e)
            return None
        
    def post(self, request, id):
        # Get doctor
        doctor = self.get_doctor(request)

        if not doctor:
            return Response({"error": "Unauthorized"}, status=status.HTTP_404_NOT_FOUND)
        
        # Find appointment
        appointment = Appointment.objects(id=ObjectId(id)).first()

        if not appointment:
            return Response({
                "error": "Appointment not found"
            })
        
        if appointment.doctor.id != doctor.id:
            return Response({
                "error": "You are not authorized to handle this appointment"
            }, status=403)
        
        if appointment.status != "scheduled":
            return Response({
                "error": "You can only handle scheduled appointments"
            }, status=403)
        
        # Take data
        serializer = DiagnosisSerializer(
            data=request.data, 
            context={"appointment": appointment}
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Handle appointment
        serializer.save()

        # Update appointment status
        appointment.status = "finished"
        appointment.save()

        # Response
        return Response({
            "message": "Appointment handled"
        }, status=status.HTTP_200_OK)