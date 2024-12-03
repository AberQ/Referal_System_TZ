from django.contrib.auth.backends import ModelBackend
from .models import CustomUser

class PhoneAuthBackend(ModelBackend):
    def authenticate(self, request, phone_number=None, code=None):
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
            if user.check_password(code):  # Вместо пароля используйте код
                return user
        except CustomUser.DoesNotExist:
            return None
