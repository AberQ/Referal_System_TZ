from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import random
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, referred_by=None, **extra_fields):
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
        
        # Если указан реферальный код, сохраняем его
        if referred_by:
            user.referred_by = referred_by
        
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
    phone_number = models.CharField(
        max_length=15, 
        unique=True,
        validators=[RegexValidator(
            regex=r'^\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$', 
            message="Введите правильный номер телефона."
        )]
    )
    auth_code = models.CharField(max_length=4, blank=True, null=True, unique=True)  # Уникальный код
    referral_code = models.CharField(max_length=6, blank=True, null=True, unique=True)  # Уникальный реферальный код
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referred_users')  # Кто пригласил
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
        
        # Проверка, что у пользователя не может быть больше одного пригласившего
        if self.referred_by and self.referred_by == self:
            raise ValidationError("A user cannot refer themselves.")
        
        super().save(*args, **kwargs)

    def clean(self):
        # Проверка, что у пользователя не может быть более одного пригласившего
        if self.referred_by and self.referred_by == self:
            raise ValidationError("A user cannot refer themselves.")
    def get_jwt_token(self):
        """
        Генерация JWT-токена с добавлением phone_number, auth_code и referral_code.
        """
        refresh = RefreshToken.for_user(self)
        
        # Добавление дополнительных данных в payload
        refresh.payload.update({
            'phone_number': self.phone_number,
            'auth_code': self.auth_code,
            'referral_code': self.referral_code,
            'referred_by': self.referred_by.phone_number if self.referred_by else None  
        })
        
        return str(refresh.access_token)