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
class PhoneNumberFormView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'phone_number_form.html')


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

def auth_page(request):
    return render(request, 'auth.html')

class ProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Возвращает профиль пользователя с его рефералами.
        """
        # Получаем текущего аутентифицированного пользователя
        user = request.user

        # Сериализуем профиль пользователя
        serializer = UserProfileSerializer(user)

        return Response(serializer.data)


class ReferralCodeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # Требуем аутентификацию

    def post(self, request):
        """
        Позволяет авторизованному пользователю ввести чужой referral_code и заполнить поле referred_by.
        """
        referral_code = request.data.get('referral_code')

        # Проверяем, что referral_code передан в запросе
        if not referral_code:
            return Response({"detail": "Referral code is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем, что пользователь не пытается ввести свой собственный реферальный код
        if referral_code == request.user.referral_code:
            raise PermissionDenied({"detail": "You cannot use your own referral code."})

        # Ищем пользователя с данным referral_code
        try:
            referred_user = CustomUser.objects.get(referral_code=referral_code)
        except CustomUser.DoesNotExist:
            raise NotFound({"detail": "User with this referral code not found."})

        # Если пользователь уже имеет поле referred_by, возвращаем ошибку
        if request.user.referred_by:
            return Response({"detail": "You have already been referred by someone."}, status=status.HTTP_400_BAD_REQUEST)

        # Обновляем поле referred_by для текущего пользователя
        request.user.referred_by = referred_user
        request.user.save()

        return Response({"detail": "Referral code applied successfully."}, status=status.HTTP_200_OK)





@login_required
def referral_code_view(request):
    """
    Отображает страницу ввода реферального кода.
    """
    return render(request, 'referral_code.html')




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
