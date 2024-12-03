from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('phone_number', 'is_active', 'is_staff', 'is_superuser')

    def clean_password1(self):
        # Возвращаем пустое значение, чтобы не требовать пароль
        return None

    def save(self, commit=True):
        user = super().save(commit=False)
        if not user.password:
            user.set_unusable_password()  # Устанавливаем невозможный пароль
        if commit:
            user.save()
        return user
