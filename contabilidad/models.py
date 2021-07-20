from conductor.models import Vehiculo
import uuid
from django.db import models
from django.db.models.enums import Choices

# Create your models here.

MESES = (
    (1, 'ENERO'),
    (2, 'FEBRERO'),
    (3, 'MARZO'),
    (4, 'ABRIL'),
    (5, 'MAYO'),
    (6, 'JUNIO'),
    (7, 'JULIO'),
    (8, 'AGOSTO'),
    (9, 'SEPTIEMBRE'),
    (10, 'OCTUBRE'),
    (11, 'NOVIEMBRE'),
    (12, 'DICIEMBRE'),
)


class PagoEquipoPesado(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mes = models.IntegerField(choices=MESES, default=1)
    gestion = models.IntegerField(default=0)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    total = models.FloatField(default=0.0)
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
