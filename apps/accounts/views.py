from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializers
from .serializers import LoginSerializers
from .serializers import UpdateSerializers
from django.contrib.auth.hashers import check_password
from .models import User
from .utils import generate_jwt
from bson import ObjectId
import jwt
from django.conf import settings

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        # Take data
        serializer = RegisterSerializers(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        # create user
        user = serializer.save()

        # Response
        return Response({
            "id": str(user.id),
            "username": user.username
        }, status=status.HTTP_201_CREATED)
    
class LoginView(APIView):
    def post(self, request):
        # Take data
        serializers = LoginSerializers(data=request.data)

        # Validate based on serializers
        if not serializers.is_valid():
            return Response(serializers.errors, status=400)
        
        # Get username and password
        username = serializers.validated_data["username"]
        password = serializers.validated_data["password"]

        # Find the user
        user = User.objects(username=username).first()

        # If user not found
        if not user:
            return Response({
                "error": "User not found"
            }, status=404)
        
        # Password check
        if not check_password(password, user.password):
            return Response({
                "error": "Wrong password"
            }, status=401)
        
        token = generate_jwt(user)

        return Response ({
            "token": token,
            "user_id": str(user.id),
            "username": user.username
        }, status=200)
    
class UpdateView(APIView):

    def get_token(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None

        try:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")

            return User.objects(id=ObjectId(user_id)).first()
        except Exception as e:
            print(e)
            return None
    
    def put(self, request):

        user = self.get_token(request)        
        if not user:
            return Response({
                "error": "User not found"
            }, status=401)

        # Take data
        serializers = UpdateSerializers(
            instance=user,
            data=request.data,
            context={"user_id": str(user.id)}
        )

        # Validate based on serializers
        if not serializers.is_valid():
            return Response(serializers.errors, status=400)
        
        # Update user
        user = serializers.save()

        return Response({
            "id": str(user.id),
            "username": user.username
        }, status=200)