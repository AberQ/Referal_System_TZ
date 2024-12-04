from django.contrib import admin
from django import forms
from .models import *
from django.contrib.auth.forms import UserChangeForm

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('phone_number', 'is_active', 'is_staff', 'is_superuser', 'referred_by')

    
    def clean_password(self):
        return None  

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('phone_number', 'is_active', 'is_staff', 'is_superuser', 'referred_by')

class CustomUserAdmin(admin.ModelAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('phone_number', 'auth_code', 'referral_code', 'referred_by', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('phone_number',)
    readonly_fields = ('auth_code', 'referral_code')  

    
    add_fieldsets = (
        (None, {
            'fields': ('phone_number', 'is_active', 'is_staff', 'is_superuser', 'referred_by'),
        }),
    )

   
    def save_model(self, request, obj, form, change):
        if not obj.auth_code: 
            obj.auth_code = CustomUserManager().generate_unique_auth_code()  
        if not obj.referral_code:  
            obj.referral_code = CustomUserManager().generate_unique_referral_code() 
        super().save_model(request, obj, form, change)

admin.site.register(CustomUser, CustomUserAdmin)
