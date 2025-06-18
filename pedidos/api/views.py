from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from pedidos.api.permissions import IsGerente
from pedidos.models import ItemPedido, Pedido
from pedidos.api.serializers import ItemPedidoSerializer, PedidoFinalizadoSerializer, PedidoSerializer, PedidoSerializerList

class ItemPedidoView(ModelViewSet):
    serializer_class = ItemPedidoSerializer
    queryset = ItemPedido.objects.all()
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = ItemPedidoSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_item = ItemPedido.objects.create(
                produto=serializer.validated_data['produto'],
                marca=serializer.validated_data['marca'],
                valor=serializer.validated_data['valor'],
                quantidade=serializer.validated_data['quantidade']
            )
            serializer_resp = ItemPedidoSerializer(new_item)
            return Response({"Info":"Sucesso ao cadastrar novo produto", "data":serializer_resp.data}, status=status.HTTP_201_CREATED)
        
    
    @action(methods=["get"], detail=False, url_path="teste1")
    def metodo1(self, request, *args, **kwargs):
        return Response({"Info": "Este é o retorno de um método personalizado"}, status=status.HTTP_200_OK)
    
    @action(methods=["get"], detail=True, url_path="teste2")
    def metodo2(self, request, *args, **kwargs):
        item = self.get_object()
        return Response({"Info": "Este é o retorno de um método personalizado com passagem de objeto", "data": item.produto})
    

class PedidoView(ModelViewSet):
    serializer_class = PedidoSerializer
    queryset = Pedido.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = PedidoSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            novo_pedido = Pedido.objects.create(
                cliente=serializer.validated_data['cliente'],
                data=serializer.validated_data['data'],
                valor_total=0,
                status="Pendente"
            )
            serializer_resp = PedidoSerializer(novo_pedido)
        return Response({"Info": "Novo pedido criado!", "data":serializer_resp.data}, status=status.HTTP_201_CREATED)
    
    @action(methods=['post'], detail=True, url_path="novo_item")
    def adicionar_item(self, request, *args, **kwargs):
        pedido = self.get_object()
        serializer = ItemPedidoSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_item = ItemPedido.objects.create(
                produto=serializer.validated_data['produto'],
                marca=serializer.validated_data['marca'],
                valor=serializer.validated_data['valor'],
                quantidade=serializer.validated_data['quantidade']
            )
            pedido.itens.add(new_item)
            serializer_resp = PedidoSerializerList(pedido)
            return Response({"Info":"Sucesso ao adicionar novo item!", "data":serializer_resp.data}, status=status.HTTP_200_OK)
    
    @action(methods=['get'], detail=True, url_path="finalizado")
    def finalizar_pedido(self, request, *args, **kwargs):
        pedido = self.get_object()
        for item in pedido.itens.all():
            pedido.valor_total+=item.valor*item.quantidade
        pedido.status="Finalizado"
        serializer_resp = PedidoFinalizadoSerializer(pedido)
        return Response({"Info":"Pedido Finalizado!", "data":serializer_resp.data}, status=status.HTTP_200_OK)