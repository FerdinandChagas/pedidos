from rest_framework import serializers
from pedidos.models import ItemPedido, Pedido
from users.api.serializers import UserSerializer

class ItemPedidoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemPedido
        fields = ["produto", "marca", "valor", "quantidade"]

class PedidoCadastroSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pedido
        fields = ['id','data','cliente']

class PedidoSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Pedido
        fields = ['id','data','cliente','user','status']

class PedidoSerializerList(serializers.ModelSerializer):
    

    class Meta:
        model = Pedido
        fields = ['id','data','cliente','itens','user','status']

class PedidoFinalizadoSerializer(serializers.ModelSerializer):
    itens=ItemPedidoSerializer(many=True)

    class Meta:
        model = Pedido
        fields = ['id','data','cliente','itens','valor_total','status']