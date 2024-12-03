from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import random

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone Number field must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        
        # Генерация уникального кода для пользователя
        user.auth_code = self.generate_unique_auth_code()
        
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, password, **extra_fields)

    def generate_unique_auth_code(self):
        """
        Генерация уникального 4-значного кода.
        """
        while True:
            code = str(random.randint(1000, 9999))  # Генерируем случайный 4-значный код
            if not CustomUser.objects.filter(auth_code=code).exists():  # Проверяем, что код уникален
                return code

class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=15, unique=True)
    auth_code = models.CharField(max_length=4, blank=True, null=True, unique=True)  # Поле для 4-значного кода
    password = models.CharField(max_length=128, blank=True, null=True)  # Сделаем пароль необязательным
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []  # Нет необходимости в пароле для обычных пользователей

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number

    def save(self, *args, **kwargs):
        # Если у пользователя нет пароля, устанавливаем невозможный
        if not self.password:
            self.set_unusable_password()
        super().save(*args, **kwargs)
