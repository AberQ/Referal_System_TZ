from rest_framework import serializers
from .models import *

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('phone_number', 'auth_code')

class UserProfileSerializer(serializers.ModelSerializer):
   
    referred_by = serializers.CharField(source='referred_by.phone_number', default=None)
    referred_users = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'phone_number', 'auth_code', 'referral_code', 'referred_by', 'referred_users')

    def get_referred_users(self, obj):
        """
        Возвращает список номеров телефонов пользователей, которые были приглашены текущим пользователем.
        """
        referred_users = CustomUser.objects.filter(referred_by=obj)
        return [user.phone_number for user in referred_users]
