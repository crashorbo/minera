from django.contrib import admin
from pesaje.models import Muestra

# Register your models here.
class MuestraAdmin(admin.ModelAdmin):
    search_fields = ['codigo',]
    
admin.site.register(Muestra, MuestraAdmin)