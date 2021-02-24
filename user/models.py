import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from django.db.models.query import QuerySet

# Create your models here.
TIPO_ROL = (
    (0, 'GERENTE'),
    (1, 'ADMINISTRACION'),
    (2, 'PESAJE'),
    (3, 'LABORATORIO'),
    (4, 'CONTABILIDAD'),
)

TIPO_PARAMETRO = (
    (0, 'COLOR'),
)


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    photo = models.ImageField(
        upload_to='users/avatars/', null=True, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    rol = models.IntegerField(choices=TIPO_ROL, default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def clean(self):
        self.first_name = self.first_name.upper()
        self.last_name = self.last_name.upper()


class Parametro(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tipo = models.IntegerField(choices=TIPO_PARAMETRO, default=0)
    nombre = models.CharField(max_length=255)
    valor = models.CharField(max_length=255)
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Cotizacion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    valor = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Destino(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def clean(self):
        self.nombre = self.nombre.upper()

    def __str__(self):
        return self.nombre
