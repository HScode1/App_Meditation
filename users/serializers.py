from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'timezone', 'level', 
                 'daily_goal', 'last_login_at', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at', 'last_login_at')
