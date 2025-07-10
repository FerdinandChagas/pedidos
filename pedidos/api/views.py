"""Módulo de Views do APP Pedidos"""
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from pedidos.api.permissions import IsGerente, IsCliente
from pedidos.models import ItemPedido, Pedido
from pedidos.api.serializers import (
    ItemPedidoSerializer,
    PedidoCadastroSerializer,
    PedidoFinalizadoSerializer,
    PedidoSerializer,
    PedidoSerializerList)

# pylint: disable=no-member
# pylint: disable=too-many-ancestors


class ItemPedidoView(ModelViewSet):
    """ View de requisições para Item do Pedido """
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
            return Response(
                {"Info": "Sucesso ao cadastrar novo produto",
                 "data": serializer_resp.data},
                status=status.HTTP_201_CREATED)
        return Response(
            {"Info": "Falha ao cadastrar novo produto"},
            status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["get"], detail=False, url_path="teste1")
    def metodo1(self):
        """Exemplo de método sem objeto referenciado (detail=False)"""
        return Response(
            {"Info": "Este é o retorno de um método personalizado"},
            status=status.HTTP_200_OK)

    @action(methods=["get"], detail=True, url_path="teste2")
    def metodo2(self):
        """Exemplo de método com objeto referenciado (detail=True)"""
        item = self.get_object()

        return Response(
            {"Info": "Este é o retorno de um "
                     "método personalizado com passagem "
                     "de objeto", "data": item.produto})


class PedidoView(ModelViewSet):
    """View de requisições para Pedido"""
    serializer_class = PedidoSerializer
    permission_classes = [IsCliente | IsGerente]

    def create(self, request, *args, **kwargs):
        serializer = PedidoCadastroSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            novo_pedido = Pedido.objects.create(    # pylint: disable=no-member
                cliente=serializer.validated_data['cliente'],
                data=serializer.validated_data['data'],
                valor_total=0,
                status="Pendente"
            )
            novo_pedido.user = request.user
            novo_pedido.save()
            serializer_resp = PedidoSerializer(novo_pedido)
            return Response(
                {"Info": "Novo pedido criado!",
                 "data": serializer_resp.data},
                status=status.HTTP_201_CREATED)
        return Response(
                {"Info": "Falha ao criar um novo pedido!"},
                status=status.HTTP_201_CREATED)

    def nova_funcao(self, *args, **kwargs):
        """Exemplo de função utilizando parâmetros
           referenciados (args, kwargs)"""
        # nova_funcao(15, 18, 45, 28, 70, nome="Ferdinandy", cargo="Professor")
        print(kwargs['nome'])
        return args[0]+args[1]

    @action(methods=['post'], detail=True, url_path="novo_item")
    def adicionar_item(self, request):
        """Método para adicionar um Item ao Pedido"""
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
            return Response(
                {"Info": "Sucesso ao adicionar novo item!",
                 "data": serializer_resp.data},
                status=status.HTTP_200_OK)
        return Response(
                {"Info": "Falha ao tentar adicionar novo item!"},
                status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True, url_path="finalizado")
    def finalizar_pedido(self):
        """Método para finalizar o Pedido"""
        pedido: Pedido = self.get_object()
        pedido = self.calcular_total(pedido)
        pedido.status = "Finalizado"
        pedido.save()
        serializer_resp = PedidoFinalizadoSerializer(pedido)
        return Response(
            {"Info": "Pedido Finalizado!",
             "data": serializer_resp.data},
            status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsGerente]
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Cliente"):
            return Pedido.objects.filter(user=user)
        return Pedido.objects.all()

    def calcular_total(self, pedido):
        """Método para calcular o total do pedido"""
        try:
            for item in pedido.itens.all():
                pedido.valor_total += item.valor*item.quantidade
            pedido.valor_total -= pedido.valtotalor_*0.05
            return pedido
        except TypeError:
            return 0
