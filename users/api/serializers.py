from django.contrib.auth.models import User
from rest_framework import serializers
from users.models import UserProfileExample


class UserProfileExampleSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfileExample
        fields = ['id', 'address', 'phone_number', 'birth_date', 'user']

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["username", "password"]
