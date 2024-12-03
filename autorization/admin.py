from django.contrib import admin
from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserChangeForm

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('phone_number', 'is_active', 'is_staff', 'is_superuser')
    
    # Переопределяем метод clean_password, чтобы не требовать пароля
    def clean_password(self):
        return None  # Пароль не требуется

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('phone_number', 'is_active', 'is_staff', 'is_superuser')

class CustomUserAdmin(admin.ModelAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('phone_number', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('phone_number',)

    # Настроим поля для добавления нового пользователя
    add_fieldsets = (
        (None, {
            'fields': ('phone_number', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
