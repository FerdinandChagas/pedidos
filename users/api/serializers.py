from django.contrib.auth.models import User, Group
from rest_framework import serializers
from users.models import UserProfileExample


class UserProfileExampleSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfileExample
        fields = ['id', 'address', 'phone_number', 'birth_date', 'user']

class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(many=True, read_only=True,slug_field="name")
    class Meta:
        model = User
        fields = ["username", "password", "groups"]
