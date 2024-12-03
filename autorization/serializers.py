from rest_framework import serializers
from .models import *

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('phone_number', 'auth_code')
        
class UserProfileSerializer(serializers.ModelSerializer):
    # Сериализуем поле referred_by (если есть)
    referred_users = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'phone_number', 'auth_code', 'referral_code', 'referred_by', 'referred_users')

    def get_referred_users(self, obj):
        """
        Возвращает список ID пользователей, которые были приглашены текущим пользователем.
        """
        referred_users = CustomUser.objects.filter(referred_by=obj)
        return [user.id for user in referred_users]