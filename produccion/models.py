import uuid
from django.db import models

# Create your models here.


class Produccion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    minima_ley = models.FloatField(default=0)
    maxima_ley = models.FloatField(default=0)
    destino = models.CharField(max_length=200)
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
