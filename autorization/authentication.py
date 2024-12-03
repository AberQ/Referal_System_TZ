from django.contrib.auth.backends import ModelBackend
from .models import CustomUser

class PhoneAuthBackend(ModelBackend):
    def authenticate(self, request, phone_number=None, code=None, password=None):
        try:
            # Находим пользователя по номеру телефона
            user = CustomUser.objects.get(phone_number=phone_number)
            
            # Для администраторов проверяем пароль, если он задан
            if user.is_staff and password:
                if not user.check_password(password):  # Для администраторов проверяем пароль
                    return None
            
            # Для обычных пользователей проверяем код, если он задан
            if not user.is_staff and code:
                session_code = request.session.get('auth_code')  # Код, который был сгенерирован и сохранен в сессии
                if session_code != code:
                    return None

            # Если все проверки прошли успешно, возвращаем пользователя
            return user

        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        """
        Получаем пользователя по его ID
        """
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
