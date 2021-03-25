from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.LaboratorioIndexView.as_view(), name='laboratorio-index'),
    url(r'^list/json/$',
        views.LaboratorioListJson.as_view(), name='laboratorio-json'),
    path('update/<pk>/', views.LaboratorioUpdateView.as_view(),
         name='laboratorio-update'),
    path('generar/laboratorios/<pk>/', views.LaboratorioGenerarView.as_view(),
         name='laboratorios-generar'),
    path('muestras/list/<pk>/', views.MuestrasListView.as_view(),
         name='muestras-list'),
    path('muestra/update/<pk>/', views.MuestraUpdateView.as_view(),
         name='muestra-update')
]
