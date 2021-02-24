from django.urls import path
from django.conf.urls import url

from .views import ProveedorListJson, ProveedorTemplateView, ProveedorCreateView, ProveedorEditView, ProveedorAutocomplete

urlpatterns = [
    path('', ProveedorTemplateView.as_view(), name='proveedor-index'),
    url(r'^list/json/$',
        ProveedorListJson.as_view(), name='proveedor-json'),
    url(r'^proveedor-autocomplete/$', ProveedorAutocomplete.as_view(),
        name='proveedor-autocomplete'),
    path('create/', ProveedorCreateView.as_view(), name='proveedor-create'),
    path('edit/<pk>', ProveedorEditView.as_view(), name='proveedor-edit'),
]
