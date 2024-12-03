from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import random

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        """
        Создаем пользователя с номером телефона и паролем
        """
        if not phone_number:
            raise ValueError('The Phone Number field must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        
        # Генерация уникальных кодов
        user.auth_code = self.generate_unique_auth_code()
        user.referral_code = self.generate_unique_referral_code()
        
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        """
        Создаем суперпользователя с номером телефона и паролем
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, password, **extra_fields)

    def generate_unique_auth_code(self):
        """
        Генерация уникального 4-значного кода.
        """
        while True:
            code = str(random.randint(1000, 9999))  # Генерация случайного 4-значного кода
            if not CustomUser.objects.filter(auth_code=code).exists():  # Проверяем, что код уникален
                return code

    def generate_unique_referral_code(self):
        """
        Генерация уникального 6-значного реферального кода.
        """
        while True:
            code = str(random.randint(100000, 999999))  # Генерация случайного 6-значного кода
            if not CustomUser.objects.filter(referral_code=code).exists():  # Проверяем, что код уникален
                return code

class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=15, unique=True)
    auth_code = models.CharField(max_length=4, blank=True, null=True, unique=True)  # Уникальный код
    referral_code = models.CharField(max_length=6, blank=True, null=True, unique=True)  # Уникальный реферальный код
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []  # Нет необходимости в пароле для обычных пользователей

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number

    def save(self, *args, **kwargs):
        if not self.password:
            self.set_unusable_password()
        super().save(*args, **kwargs)