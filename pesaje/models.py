import uuid
from django.db import models

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
    peso_bruto = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    peso_tara = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    peso_neto = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    peso_neto_tn = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    numero = models.CharField(max_length=20, unique=True)
    pesaje = models.BooleanField(default=False)
    numero_paleta = models.CharField(max_length=10, default='')
    color = models.CharField(max_length=50, default='')
    paleta = models.BooleanField(default=False)
    laboratorio = models.BooleanField(default=False)
    au = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    h2o = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    porcentaje_tamanos = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    cobre_soluble = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    tipo_carga = models.CharField(
        max_length=10, choices=TIPO_CARGA, default='NORMAL')
    tms = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    tms_neta = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    tms_penalizar = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    tms_pagar = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    finos_gr = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    finos_gr_recup = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    finos_oz = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    cotizacion = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    calculo_regalia = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    recu_planta = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    valor_venta = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    consto_tratamiento = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    total_liquidacion_prov = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    regalia = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    penalizacion_cu_soluble = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    # desde este punto pago de contador
    anticipo = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    equipo_pesado = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    balanza = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    volqueta = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    analisis_laboratorio = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    otros_descuentos = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    retencion_acuerdo = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    retencion_acuerdo_vol = models.BooleanField(default=False)
    valor_reposicion = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    total_descuento = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    liquido_pagable = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
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
    malla_mas = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    malla_menos = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    ley_ponderada = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    nro_certif = models.CharField(max_length=20, default='')
    laboratorio = models.ForeignKey(
        Laboratorio, on_delete=models.CASCADE, null=True)
    css_class = models.CharField(max_length=20, default='')
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
