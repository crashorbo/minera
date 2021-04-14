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
    (1, 'NUMERACION'),
    (2, 'CODIGO'),
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
    valor_oficial = models.FloatField(default=0)
    valor_pagable = models.FloatField(default=0)
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Origen(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def clean(self):
        self.nombre = self.nombre.upper()

    def __str__(self):
        return self.nombre


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


class Laboratorio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=200)
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    def clean(self):
        self.nombre = self.nombre.upper()


class Generador(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cantidad = models.IntegerField(default=0)
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class CodigoMixin(object):

    def q_for_search_word(self, word):
        return Q(numero__icontains=word) & Q(utilizado=False)

    def q_for_search(self, search):
        q = Q()
        if search:
            searches = search.split()
            for word in searches:
                q = q & self.q_for_search_word(word)
        return q

    def filter_on_search(self, search):
        return self.filter(self.q_for_search(search))


class CodigoQuerySet(QuerySet, CodigoMixin):
    pass


class CondigoManager(models.Manager, CodigoMixin):

    def get_queryset(self):
        return CodigoQuerySet(self.model, using=self._db)


class Codigo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    numero = models.CharField(max_length=100)
    cod_externo = models.CharField(max_length=100)
    cod_proveedor = models.CharField(max_length=100)
    cod_testigo = models.CharField(max_length=100)
    cod_bolsa = models.CharField(max_length=100)
    generador = models.ForeignKey(Generador, on_delete=models.CASCADE)
    utilizado = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = CondigoManager()


class Factor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rango_inferior = models.FloatField(default=0)
    rango_superior = models.FloatField(default=0)
    factor_recuperacion = models.FloatField(default=0)
    sugerencia = models.FloatField(default=0)
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
