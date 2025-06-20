from rest_framework.permissions import BasePermission

from pedidos.models import Pedido

class IsGerente(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='Gerente').exists()

class IsCliente(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='Cliente').exists()
    
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Pedido):
            return obj.user == request.user
        return super().has_object_permission(request, view, obj)