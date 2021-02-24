import re
from django import template
from django.urls import reverse, NoReverseMatch
register = template.Library()


@register.simple_tag(takes_context=True)
def active(context, pattern_or_urlname):
    try:
        pattern = '^' + reverse(pattern_or_urlname)
    except NoReverseMatch:
        pattern = pattern_or_urlname
    path = context['request'].path
    if re.search(pattern, path):
        return 'active'
    return ''


@register.filter
def rol_usuario(val):
    TIPO_ROL = {
        0: 'GERENTE',
        1: 'ADMINISTRACION',
        2: 'PESAJE',
        3: 'LABORATORIO',
        4: 'CONTABILIDAD'
    }
    return TIPO_ROL[val]


@register.filter
def color_parametro(val):
    TIPO_COLOR = {
        '1': 'ENERO',
        '2': 'FEBRERO',
        '3': 'MARZO',
        '4': 'ABRIL',
        '5': 'MAYO',
        '6': 'JUNIO',
        '7': 'JULIO',
        '8': 'AGOSTO',
        '9': 'SEPTIEMBRE',
        '10': 'OCTUBRE',
        '11': 'NOVIEMBRE',
        '12': 'DICIEMBRE'
    }
    return TIPO_COLOR[val]
