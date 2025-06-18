from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ItemPedido(models.Model):
    produto = models.CharField(max_length=40)
    marca = models.CharField(max_length=40)
    valor = models.FloatField()
    quantidade = models.IntegerField()

class Pedido(models.Model):
    itens=models.ManyToManyField(ItemPedido, default=None)
    data=models.DateField()
    ##usuario=models.ForeignKey(User, on_delete=models.CASCADE)
    cliente=models.CharField(max_length=120)
    valor_total=models.FloatField()
    status=models.CharField(max_length=20)