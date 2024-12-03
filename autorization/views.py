from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import login
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import NotFound
from .serializers import *
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.exceptions import PermissionDenied
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

def home(request):
    return render(request, 'phone_number_form.html')


class GetOrCreateUser(APIView):
    @swagger_auto_schema(
        operation_description="Создает пользователя по номеру телефона или возвращает auth_code для существующего пользователя.",
        operation_summary="Создание пользователя или возврат auth_code для существующего.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            
            properties={
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='Номер телефона пользователя')
            }
        ),
        responses={
            200: openapi.Response('User exists', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'auth_code': openapi.Schema(type=openapi.TYPE_STRING)})),
            201: openapi.Response('User created', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'auth_code': openapi.Schema(type=openapi.TYPE_STRING)})),
            400: openapi.Response('Bad Request', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)})),
        }
    )
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Попытка найти пользователя по номеру телефона
        user = CustomUser.objects.filter(phone_number=phone_number).first()

        if user:
            return Response({"auth_code": user.auth_code}, status=status.HTTP_200_OK)
        else:
            user = CustomUser.objects.create_user(phone_number=phone_number)
            return Response({"auth_code": user.auth_code}, status=status.HTTP_201_CREATED)




class AuthenticateUser(APIView):
    @swagger_auto_schema(
        operation_description="Аутентифицирует пользователя по auth_code и генерирует JWT токен.",
        operation_summary="Аутентификация пользователя по auth_code и генерация JWT токена.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'auth_code': openapi.Schema(type=openapi.TYPE_STRING, description='Код подтверждения для аутентификации')
            }
        ),
        responses={
            200: openapi.Response('Token generated', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'token': openapi.Schema(type=openapi.TYPE_STRING)})),
            400: openapi.Response('Invalid auth code', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'error': openapi.Schema(type=openapi.TYPE_STRING)})),
        }
    )
    def post(self, request, *args, **kwargs):
        auth_code = request.data.get('auth_code')

        if not auth_code:
            return Response({"error": "Auth code is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.filter(auth_code=auth_code).first()

        if user:
            token = user.get_jwt_token()
            return Response({"token": token}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid auth code"}, status=status.HTTP_400_BAD_REQUEST)


def auth_page(request):
    return render(request, 'auth.html')

class ProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary="Получение профиля пользователя.",
        operation_description="Этот метод возвращает информацию о текущем профиле пользователя, включая данные о его рефералах.",
        responses={200: openapi.Response('Profile data', UserProfileSerializer)},
    )
    def get(self, request):
        """
        Возвращает профиль пользователя с его рефералами, если пользователь авторизован.
        """
        # Получаем текущего аутентифицированного пользователя
        user = request.user

        # Сериализуем профиль пользователя
        serializer = UserProfileSerializer(user)

        return Response(serializer.data)


class ReferralCodeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Позволяет пользователю ввести чужой реферальный код.",
        operation_summary="Применение реферального кода.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'referral_code': openapi.Schema(type=openapi.TYPE_STRING, description='Реферальный код')
            }
        ),
        responses={
            200: openapi.Response('Referral code applied successfully'),
            400: openapi.Response('Bad Request', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'detail': openapi.Schema(type=openapi.TYPE_STRING)})),
            404: openapi.Response('Referral code not found'),
            403: openapi.Response('Permission Denied'),
        }
    )
    def post(self, request):
        referral_code = request.data.get('referral_code')

        if not referral_code:
            return Response({"detail": "Referral code is required."}, status=status.HTTP_400_BAD_REQUEST)

        if referral_code == request.user.referral_code:
            raise PermissionDenied({"detail": "You cannot use your own referral code."})

        try:
            referred_user = CustomUser.objects.get(referral_code=referral_code)
        except CustomUser.DoesNotExist:
            raise NotFound({"detail": "User with this referral code not found."})

        if request.user.referred_by:
            return Response({"detail": "You have already been referred by someone."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.referred_by = referred_user
        request.user.save()

        return Response({"detail": "Referral code applied successfully."}, status=status.HTTP_200_OK)







def referral_code_view(request):
    """
    Отображает страницу ввода реферального кода.
    """
    return render(request, 'referral_code.html')

def profile_page(request):
    return render(request, 'profile.html')


class UserProfilePageView(LoginRequiredMixin, TemplateView):
    """
    Рендеринг HTML-страницы профиля пользователя.
    """
    template_name = "profile.html"

    # Можно передать дополнительные параметры в контекст, если требуется
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Профиль пользователя"  # Пример добавления данных
        return context
