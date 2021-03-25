from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.ContabilidadIndexView.as_view(), name='contabilidad-index'),
    url(r'^list/json/$',
        views.ContabilidadListJson.as_view(), name='contabilidad-json'),
    path('update/<pk>/', views.ContabilidadUpdateView.as_view(),
         name='contabilidad-update'),
    # path('generar/laboratorios/<pk>/', views.LaboratorioGenerarView.as_view(),
    #      name='laboratorios-generar'),
    # path('muestras/list/<pk>/', views.MuestrasListView.as_view(),
    #      name='muestras-list'),
    # path('muestra/update/<pk>/', views.MuestraUpdateView.as_view(),
    #      name='muestra-update')
]
