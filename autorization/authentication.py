from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User

class NoPasswordAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            # Дополнительная проверка (например, через код или другие данные)
            return user
        except User.DoesNotExist:
            return None
