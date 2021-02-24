from .models import Parametro
import datetime


def get_numeracion():
    today = datetime.date.today()
    try:
        parametro = Parametro.objects.get(tipo=1, nombre=today.year)
    except Parametro.DoesNotExist:
        parametro = Parametro(tipo=1, nombre=today.year, valor=0)
        parametro.save()
    parametro.valor = int(parametro.valor)+1
    parametro.save()
    return transformar_numeracion(parametro.nombre, parametro.valor)


def transformar_numeracion(nombre, valor):
    nombre_corto = nombre[2:4]
    aux = '{}{}'.format(nombre_corto, ('0'*6+str(valor))[-6:])
    return aux
