from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.ContabilidadIndexView.as_view(), name='contabilidad-index'),
    path('update/<pk>/', views.ContabilidadUpdateView.as_view(),
         name='contabilidad-update'),
    path('pagar-carga/', views.ContabilidadPagarView.as_view(),
         name='contabilidad-pagar'),
    path('detalle/<pk>', views.ContabilidadCargaView.as_view(),
         name='contabilidad-carga-view'),
    path('ajax/detalle/<pk>', views.AjaxCargaDetailView.as_view(),
         name='carga-ajax-detail'),
    path('reporte/boletas/',
         views.ReporteBoletaView.as_view(), name='reporte-boleta'),
    path('reporte/comprobantes/',
         views.ReporteComprobanteView.as_view(), name='reporte-comprobantes'),
    # path('generar/laboratorios/<pk>/', views.LaboratorioGenerarView.as_view(),
    #      name='laboratorios-generar'),
    path('laboratorios/', views.AjaxLaboratoriosView.as_view(),
         name='laboratorios-list'),
    path('proveedor-origen/', views.AjaxProveedorOrigenView.as_view(),
         name='proveedor-origen'),
    path('reporte/por-pagar/', views.ReportePorPagar.as_view(),
         name='reporte-por-pagar'),
    path('reporte-cargas-pagadas/', views.AjaxCargasPagadasView.as_view(),
         name='reporte-cargas-pagadas'),
    path('reporte-cargas-general/', views.AjaxReporteCargasGeneral.as_view(),
         name='reporte-cargas-general')
]
