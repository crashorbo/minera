import uuid
from django.db import models
from django.db.models.base import Model
from django.db.models.fields.related import ForeignKey

# Create your models here.
from proveedor.models import Proveedor
from conductor.models import Vehiculo
from user.models import Destino


class Carga(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehiculo = models.ForeignKey(
        Vehiculo, related_name='vehiculo', on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    origen = models.CharField(max_length=200, default='')
    equipo_carguio = models.ForeignKey(
        Vehiculo, related_name='carguio', on_delete=models.CASCADE, null=True)
    destino = ForeignKey(Destino, on_delete=models.CASCADE)
    peso_bruto = models.DecimalField(
        decimal_places=3, max_digits=10, default=0.000)
    peso_tara = models.DecimalField(
        decimal_places=3, max_digits=10, default=0.000)
    peso_neto = models.DecimalField(
        decimal_places=3, max_digits=10, default=0.000)
    numero = models.CharField(max_length=20, default='')
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
