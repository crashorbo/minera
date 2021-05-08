import uuid
from django.db import models
import datetime
# Create your models here.
from proveedor.models import Proveedor
from conductor.models import Vehiculo, Conductor
from user.models import CustomUser, Destino, Laboratorio, Origen

TIPO_CARGA = (
    ('NORMAL', 'NORMAL'),
    ('LAMA', 'LAMA')
)


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
    pagado = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def clean(self):
        self.color = self.color.upper()


class Muestra(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    carga = models.ForeignKey(Carga, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, default='')
    codigo = models.CharField(max_length=20)
    malla_mas = models.FloatField(default=0)
    malla_menos = models.FloatField(default=0)
    ley_ponderada = models.FloatField(default=0)
    nro_certif = models.CharField(max_length=20, default='')
    laboratorio = models.ForeignKey(
        Laboratorio, on_delete=models.CASCADE, null=True)
    css_class = models.CharField(max_length=20, default='')
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
