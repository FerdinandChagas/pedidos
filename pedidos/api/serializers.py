from rest_framework import serializers
from pedidos.models import ItemPedido, Pedido

class ItemPedidoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemPedido
        fields = ["produto", "marca", "valor", "quantidade"]

class PedidoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pedido
        fields = ['id','data','cliente']

class PedidoSerializerList(serializers.ModelSerializer):

    class Meta:
        model = Pedido
        fields = ['id','data','cliente','itens']

class PedidoFinalizadoSerializer(serializers.ModelSerializer):
    itens=ItemPedidoSerializer(many=True)

    class Meta:
        model = Pedido
        fields = ['id','data','cliente','itens','valor_total']