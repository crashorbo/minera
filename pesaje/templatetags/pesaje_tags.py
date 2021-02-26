from django import template

register = template.Library()


@register.filter(name='numero_decimal')
def numero_decimal(value):
    return '{:,.3f}'.format(value).replace(",", "@").replace(".", ",").replace("@", ".")
