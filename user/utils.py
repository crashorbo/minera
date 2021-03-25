from .models import Parametro
import datetime


def get_numeracion(tipo):
    today = datetime.date.today()
    try:
        parametro = Parametro.objects.get(tipo=tipo, nombre=today.year)
        parametro.valor = int(parametro.valor)+1
        parametro.save()
    except Parametro.DoesNotExist:
        parametro = Parametro(tipo=tipo, nombre=today.year, valor=1)
        parametro.save()
    return transformar_numeracion(str(parametro.nombre), parametro.valor)


def transformar_numeracion(nombre, valor):
    nombre_corto = nombre[2:4]
    aux = '{}{}'.format(nombre_corto, ('0'*6+str(valor))[-6:])
    return aux
