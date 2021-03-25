import uuid
from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet

# Create your models here.


class MyModelMixin(object):

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


class MyModelQuerySet(QuerySet, MyModelMixin):
    pass


class MyModelManager(models.Manager, MyModelMixin):

    def get_queryset(self):
        return MyModelQuerySet(self.model, using=self._db)


class Proveedor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombres = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    numero_documento = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = MyModelManager()

    def __str__(self):
        return '{} {}'.format(self.apellidos, self.nombres)

    def clean(self):
        self.nombres = self.nombres.upper()
        self.apellidos = self.apellidos.upper()
        try:
            self.direccion = self.direccion.upper()
        except:
            self.direccion = self.direccion
