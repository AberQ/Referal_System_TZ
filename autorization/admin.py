from django.contrib import admin
from django import forms
from .models import *
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

    list_display = ('phone_number', 'auth_code', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('phone_number',)
    readonly_fields = ('auth_code',)  # Поле auth_code будет доступно только для чтения в админке

    # Настроим поля для добавления нового пользователя
    add_fieldsets = (
        (None, {
            'fields': ('phone_number', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

    # Переопределяем save_model, чтобы генерировать auth_code при создании пользователя
    def save_model(self, request, obj, form, change):
        if not obj.auth_code:  # Если код еще не был сгенерирован
            obj.auth_code = CustomUserManager().generate_auth_code()  # Генерируем новый код
        super().save_model(request, obj, form, change)

admin.site.register(CustomUser, CustomUserAdmin)
