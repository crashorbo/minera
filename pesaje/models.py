import uuid
from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
import datetime
# Create your models here.
from proveedor.models import Proveedor
from conductor.models import Vehiculo, Conductor
from user.models import CustomUser, Destino, Factor, Laboratorio, Origen

TIPO_CARGA = (
    ('NORMAL', 'NORMAL'),
    ('LAMA', 'LAMA')
)


class MyModelMixin(object):

    def q_for_search_word(self, word):
        return Q(numero__contains=word)

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


class Carga(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(
        Vehiculo, related_name='vehiculo', on_delete=models.CASCADE)
    conductor_vehiculo = models.ForeignKey(
        Conductor, related_name='conductor_vehiculo', on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    origen = models.ForeignKey(Origen, on_delete=models.CASCADE)
    equipo_carguio = models.ForeignKey(
        Vehiculo, related_name='carguio', on_delete=models.CASCADE, null=True)
    destino = models.ForeignKey(Destino, on_delete=models.CASCADE)
    peso_bruto = models.FloatField(default=0)
    peso_tara = models.FloatField(default=0)
    peso_neto = models.FloatField(default=0)
    peso_neto_tn = models.FloatField(default=0)
    numero = models.CharField(max_length=20, unique=True)
    pesaje = models.BooleanField(default=False)
    pesaje_bruto = models.BooleanField(default=True)
    pesaje_tara = models.BooleanField(default=False)
    numero_paleta = models.CharField(max_length=10, default='')
    color = models.CharField(max_length=50, default='')
    fecha_paleta = models.DateField(null=True)
    paleta = models.BooleanField(default=False)
    laboratorio = models.BooleanField(default=False)
    au = models.FloatField(default=0)
    h2o = models.FloatField(default=0)
    porcentaje_tamanos = models.FloatField(default=0)
    cobre_soluble = models.FloatField(default=0)
    tipo_carga = models.CharField(
        max_length=10, choices=TIPO_CARGA, default='NORMAL')
    tms = models.FloatField(default=0)
    tms_neta = models.FloatField(default=0)
    tms_penalizar = models.FloatField(default=0)
    tms_pagar = models.FloatField(default=0)
    finos_gr = models.FloatField(default=0)
    finos_gr_recup = models.FloatField(default=0)
    finos_oz = models.FloatField(default=0)
    cotizacion = models.FloatField(default=0)
    calculo_regalia = models.FloatField(default=0)
    recu_planta = models.FloatField(default=0)
    valor_venta = models.FloatField(default=0)
    costo_tratamiento = models.FloatField(default=0)
    total_liquidacion_prov = models.FloatField(default=0)
    regalia = models.FloatField(default=0)
    penalizacion_cu_soluble = models.FloatField(default=0)
    # desde este punto pago de contador
    anticipo = models.FloatField(default=0)
    equipo_pesado = models.FloatField(default=0)
    balanza = models.FloatField(default=0)
    volqueta = models.FloatField(default=0)
    analisis_laboratorio = models.FloatField(default=0)
    otros_descuentos = models.FloatField(default=0)
    retencion_acuerdo = models.FloatField(default=0)
    retencion_acuerdo_vol = models.BooleanField(default=False)
    valor_reposicion = models.FloatField(default=0)
    total_descuento = models.FloatField(default=0)
    liquido_pagable = models.FloatField(default=0)
    observaciones = models.TextField(blank=True)
    pagado = models.BooleanField(default=False)
    fecha_pago = models.DateTimeField(blank=True, null=True)
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = MyModelManager()

    def clean(self):
        self.color = self.color.upper()

    def calcular_total(self):
        self.tms = self.peso_neto_tn*(100 - self.h2o)/100
        if self.porcentaje_tamanos > 4:
            self.tms_neta = self.tms - \
                (self.tms * self.porcentaje_tamanos)/100
        else:
            self.tms_neta = self.tms
        if self.cobre_soluble > 800:
            self.tms_penalizar = self.tms_neta
        else:
            self.tms_penalizar = 0
        self.tms_pagar = round(
            self.tms_neta - self.tms_penalizar, 2)
        self.finos_gr = self.tms_pagar * self.au
        self.finos_oz = self.finos_gr / 31.1035
        if self.tipo_carga == 'LAMA' and self.au < 3:
            self.finos_gr_recup = 0
        else:
            factor = Factor.objects.filter(
                rango_inferior__lte=self.au, rango_superior__gte=self.au)
            if factor:
                self.finos_gr_recup = round(factor[0].factor_recuperacion *
                                            self.finos_gr, 2)
        self.calculo_regalia = self.finos_oz * self.cotizacion * 6.96
        if self.tipo_carga == 'LAMA' and self.au < 3:
            self.recu_planta = 0
        else:
            if self.tipo_carga == 'NORMAL' and self.au < 1:
                self.recu_planta = 0
            else:
                factor = Factor.objects.filter(
                    rango_inferior__lte=self.au, rango_superior__gte=self.au)
                if factor:
                    self.recu_planta = factor[0].factor_recuperacion * \
                        self.finos_oz

        self.valor_venta = round(
            self.cotizacion * self.recu_planta * 6.96 * 0.94, 0)

        if self.au >= 10:
            self.costo_tratamiento = round(
                self.valor_venta * 0.52, 0)
        else:
            self.costo_tratamiento = round(
                self.valor_venta * 0.50, 0)
        self.total_liquidacion_prov = self.valor_venta - self.costo_tratamiento

        if self.recu_planta <= 0:
            self.regalia = 0
        else:
            if self.au >= 1 and self.au <= 2:
                self.regalia = round(
                    self.calculo_regalia * 0.042 * 0.9, 0)
            else:
                self.regalia = round(
                    self.calculo_regalia * 0.042 * 1, 0)

        if self.cobre_soluble >= 150 and self.cobre_soluble <= 800:
            self.penalizacion_cu_soluble = round(
                (0.0089 * self.cobre_soluble - 1.325) * 30 * self.tms_pagar, 0)
        else:
            self.penalizacion_cu_soluble = 0

        if self.retencion_acuerdo_vol:
            self.retencion_acuerdo = round(self.costo_tratamiento * 0.05, 0)
        else:
            self.retencion_acuerdo = 0
        self.total_descuento = self.regalia + self.penalizacion_cu_soluble + self.anticipo + self.equipo_pesado + self.balanza + self.volqueta + \
            self.analisis_laboratorio + self.otros_descuentos + self.retencion_acuerdo
        self.valor_reposicion = self.total_liquidacion_prov - self.regalia
        self.liquido_pagable = self.total_liquidacion_prov - self.total_descuento


class Muestra(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    carga = models.ForeignKey(
        Carga, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, default='')
    codigo = models.CharField(max_length=20)
    malla_mas = models.FloatField(default=0)
    malla_menos = models.FloatField(default=0)
    ley_ponderada = models.FloatField(default=0)
    nro_certif = models.CharField(max_length=20, default='')
    laboratorio = models.ForeignKey(
        Laboratorio, on_delete=models.CASCADE, null=True)
    css_class = models.CharField(max_length=20, default='')
    selected = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Destare(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    peso = models.FloatField(default=0)
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
