import uuid
from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils.html import escape

# Create your models here.
TIPO_SERVICIO = (
    ('VEHICULO', 'VEHICULO'),
    ('CARGUIO', 'CARGUIO')
)


class MyModelMixin(object):

    def q_for_search_word(self, word):
        return Q(nombres__icontains=word) | Q(apellidos__icontains=word) | Q(placa__icontains=word) | Q(numero_documento__icontains=word)

    def q_for_search(self, search):
        q = Q()
        if search:
            searches = search.split()
            for word in searches:
                q = q & self.q_for_search_word(word)
        return q

    def filter_on_search(self, search):
        return self.filter(self.q_for_search(search))


class MyModelQuerySet(QuerySet, MyModelMixin):
    pass


class MyModelManager(models.Manager, MyModelMixin):

    def get_queryset(self):
        return MyModelQuerySet(self.model, using=self._db)


class Vehiculo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombres = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    numero_documento = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    placa = models.CharField(max_length=50, blank=True)
    marca = models.CharField(max_length=100, blank=True, null=True)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    tipo = models.CharField(
        max_length=20, choices=TIPO_SERVICIO, default='VEHICULO')
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = MyModelManager()

    def __str__(self):
        return '{} - {}'.format(self.placa, self.marca)

    def clean(self):
        self.nombres = self.nombres.upper()
        self.apellidos = self.apellidos.upper()
        try:
            self.placa = self.placa.upper()
        except:
            self.placa = self.placa
        try:
            self.marca = self.marca.upper()
        except:
            self.marca = self.marca
        try:
            self.modelo = self.modelo.upper()
        except:
            self.modelo = self.modelo
        try:
            self.descripcion = self.descripcion.upper()
        except:
            self.descripcion = self.descripcion


class ConductorMixin(object):

    def q_for_search_word(self, word):
        return Q(nombres__icontains=word) | Q(apellidos__icontains=word) | Q(numero_documento__icontains=word)

    def q_for_search(self, search):
        q = Q()
        if search:
            searches = search.split()
            for word in searches:
                q = q & self.q_for_search_word(word)
        return q

    def filter_on_search(self, search):
        return self.filter(self.q_for_search(search))


class ConductorQuerySet(QuerySet, ConductorMixin):
    pass


class ConductorManager(models.Manager, ConductorMixin):

    def get_queryset(self):
        return ConductorQuerySet(self.model, using=self._db)


class Conductor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombres = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    numero_documento = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = ConductorManager()

    def __str__(self):
        return '{} - {} {}'.format(self.numero_documento, self.apellidos, self.nombres)

    def clean(self):
        self.nombres = self.nombres.upper()
        self.apellidos = self.apellidos.upper()
