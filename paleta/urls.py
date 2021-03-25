from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.PaletaIndexView.as_view(), name='paleta-index'),
    url(r'^list/json/$',
        views.PaletaListJson.as_view(), name='proveedor-json'),
    path('edit/<pk>/', views.PaletaUpdateView.as_view(), name='paleta-edit')
]
