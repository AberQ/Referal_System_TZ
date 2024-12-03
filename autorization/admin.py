# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    search_fields = ['phone_number']  # Добавляем поиск по номеру телефона
    list_display = ['phone_number', 'is_staff', 'is_active']
    ordering = ['phone_number']
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'fields': ('phone_number', 'password1', 'password2')}),
    )

    # Исключаем группы и разрешения
    filter_horizontal = []
    list_filter = ['is_staff', 'is_active']

admin.site.register(CustomUser, CustomUserAdmin)
