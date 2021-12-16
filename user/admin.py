from user.models import CustomUser, Codigo
from django.contrib import admin

from .models import Codigo
# Register your models here.
admin.site.register(CustomUser)


class CodigoAdmin(admin.ModelAdmin):
    list_display=('numero', 'cod_externo', 'cod_proveedor', 'cod_testigo', 'cod_bolsa')
    search_fields = ['numero',]    
    
admin.site.register(Codigo, CodigoAdmin)

admin.site.register(Codigo)

