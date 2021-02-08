import uuid
from django.db import models
from django.db.models.base import Model

# Create your models here.


class Carga(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    peso_bruto = models.DecimalField(
        decimal_places=3, max_digits=10, default=0.000)
    peso_neto = models.DecimalField(
        decimal_places=3, max_digits=10, default=0.000)
    numero = models.IntegerField(default=0)
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.numero


class Origen(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=255)
    detalle = models.TextField(blank=True, null=True)
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    def clean(self):
        self.nombre = self.nombre.upper()


class Destino(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=255)
    detalle = models.TextField(blank=True, null=True)
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    def clean(self):
        self.nombre = self.nombre.upper()
