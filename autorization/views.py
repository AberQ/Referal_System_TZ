from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import CustomUserSerializer

class GetOrCreateUser(APIView):
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Попытка найти пользователя по номеру телефона
        user = CustomUser.objects.filter(phone_number=phone_number).first()

        if user:
            # Если пользователь существует, возвращаем его auth_code
            return Response({"auth_code": user.auth_code}, status=status.HTTP_200_OK)
        else:
            # Если пользователя нет, создаем нового
            user = CustomUser.objects.create_user(phone_number=phone_number)
            return Response({"auth_code": user.auth_code}, status=status.HTTP_201_CREATED)




class AuthenticateUser(APIView):
    def post(self, request, *args, **kwargs):
        auth_code = request.data.get('auth_code')

        if not auth_code:
            return Response({"error": "Auth code is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Ищем пользователя по auth_code
        user = CustomUser.objects.filter(auth_code=auth_code).first()

        if user:
            # Если код правильный, генерируем JWT токен
            token = user.get_jwt_token()
            return Response({"token": token}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid auth code"}, status=status.HTTP_400_BAD_REQUEST)
