from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.ContabilidadIndexView.as_view(), name='contabilidad-index'),
    url(r'^list/json/$',
        views.ContabilidadListJson.as_view(), name='contabilidad-json'),
    path('update/<pk>/', views.ContabilidadUpdateView.as_view(),
         name='contabilidad-update'),
    path('pagar/<pk>/', views.ContabilidadPagarView.as_view(),
         name='contabilidad-pagar'),
    path('detalle/<pk>', views.ContabilidadCargaView.as_view(),
         name='contabilidad-carga-view'),
    path('ajax/detalle/<pk>', views.AjaxCargaDetailView.as_view(),
         name='carga-ajax-detail'),
    path('resporte/boleta/<pk>/',
         views.ReporteBoletaView.as_view(), name='reporte-boleta'),
    path('resporte/comprobante/<pk>/',
         views.ReporteComprobanteView.as_view(), name='reporte-comprobante'),
    # path('generar/laboratorios/<pk>/', views.LaboratorioGenerarView.as_view(),
    #      name='laboratorios-generar'),
    # path('muestras/list/<pk>/', views.MuestrasListView.as_view(),
    #      name='muestras-list'),
    # path('muestra/update/<pk>/', views.MuestraUpdateView.as_view(),
    #      name='muestra-update')
    path('reporte/por-pagar/', views.ReportePorPagar.as_view(),
         name='reporte-por-pagar'),
]
