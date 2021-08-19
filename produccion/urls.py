from django.urls import path, register_converter

from . import converts, views

register_converter(converts.FloatUrlParameterConverter, 'float')


urlpatterns = [
    path('', views.ProduccionIndexView.as_view(), name='produccion-index'),
    path('nuevo/', views.ProduccionNuevoView.as_view(), name='produccion-nuevo'),
    path('produccion-cargas/<float:min>/<float:max>/<int:pagado>/',
         views.ProduccionCargasView.as_view(), name="produccion-cargas"),
    path('ver/<pk>/', views.ProduccionView.as_view(),
         name="produccion-cargas-view"),
    path('reporte/<pk>/', views.ReporteProduccion.as_view(),
         name="produccion-reporte")
]
