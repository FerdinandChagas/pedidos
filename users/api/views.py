from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from users.api.serializers import UserProfileExampleSerializer, UserSerializer

from users.models import UserProfileExample

class UserProfileExampleViewSet(ModelViewSet):
    serializer_class = UserProfileExampleSerializer
    permission_classes = [AllowAny]
    queryset = UserProfileExample.objects.all()
    http_method_names = ['get', 'put']

class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()