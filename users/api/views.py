from django.contrib.auth.models import User, Group
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from users.api.serializers import UserProfileExampleSerializer, UserSerializer

from users.models import UserProfileExample
from pedidos.api.permissions import IsGerente

class UserProfileExampleViewSet(ModelViewSet):
    serializer_class = UserProfileExampleSerializer
    permission_classes = [AllowAny]
    queryset = UserProfileExample.objects.all()
    http_method_names = ['get', 'put']

class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsGerente]
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_user = User.objects.create_user(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            cliente_group,_ = Group.objects.get_or_create(name="Cliente")
            new_user.groups.add(cliente_group)
            new_user.save()
            resp_serializer = UserSerializer(new_user)
        return Response({"Info":"Usuário cadastrado com sucesso", "data": resp_serializer.data})