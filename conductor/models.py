import uuid
from django.db import models

# Create your models here.
TIPO_SERVICIO = (
    ('VEHICULO', 'VEHICULO'),
    ('CARGUIO', 'CARGUIO')
)


class Vehiculo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombres = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    numero_documento = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    placa = models.CharField(max_length=50, unique=True)
    marca = models.CharField(max_length=100, blank=True, null=True)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    tipo = models.CharField(
        max_length=20, choices=TIPO_SERVICIO, default='CARGUIO')
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.placa, self.marca)

    def clean(self):
        self.nombres = self.nombres.upper()
        self.apellidos = self.apellidos.upper()
        self.placa = self.placa.upper()
        self.marca = self.marca.upper()
        self.modelo = self.modelo.upper()
        self.descripcion = self.descripcion.upper()
