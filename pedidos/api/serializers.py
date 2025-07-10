"""Módulo de Serializers do App Pedidos"""
from rest_framework import serializers
from pedidos.models import ItemPedido, Pedido
from users.api.serializers import UserSerializer
# pylint: disable=too-few-public-methods


class ItemPedidoSerializer(serializers.ModelSerializer):
    """Serializer baseado no modelo do Item"""
    class Meta:
        """Meta-Classe com parâmetros de configuração"""
        model = ItemPedido
        fields = ["produto", "marca", "valor", "quantidade"]


class PedidoCadastroSerializer(serializers.ModelSerializer):
    """Serializer para cadastro baseado no modelo do Pedido"""
    class Meta:
        """Meta-Classe com parâmetros de configuração"""
        model = Pedido
        fields = ['id', 'data', 'cliente']


class PedidoSerializer(serializers.ModelSerializer):
    """Serializer baseado no modelo do Pedido"""
    user = UserSerializer()

    class Meta:
        """Meta-Classe com parâmetros de configuração"""
        model = Pedido
        fields = ['id', 'data', 'cliente', 'user', 'status']


class PedidoSerializerList(serializers.ModelSerializer):
    """Serializer para listagem baseado no modelo do Pedido"""
    class Meta:
        """Meta-Classe com parâmetros de configuração"""
        model = Pedido
        fields = ['id', 'data', 'cliente', 'itens', 'user', 'status']


class PedidoFinalizadoSerializer(serializers.ModelSerializer):
    """Serializer para finalização baseado no modelo do Pedido"""
    itens = ItemPedidoSerializer(many=True)

    class Meta:
        """Meta-Classe com parâmetros de configuração"""
        model = Pedido
        fields = ['id', 'data', 'cliente', 'itens', 'valor_total', 'status']
