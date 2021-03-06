from user.models import DestinoProduccion
import uuid
from django.db import models

# Create your models here.


class Produccion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    minima_ley = models.FloatField(default=0)
    maxima_ley = models.FloatField(default=0)
    tms = models.FloatField(default=0)
    destino = models.ForeignKey(
        DestinoProduccion, on_delete=models.CASCADE)
    cargas = models.TextField(default='', blank=True)
    total_cargas = models.IntegerField(default=0)
    total_cargas_utilizadas = models.IntegerField(default=0)
    estado = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
