from django.urls import path

from . import views

urlpatterns = [
    path('', views.PesajeIndexView.as_view(), name='pesaje-index'),
    path('create/', views.PesajeCreateView.as_view(), name='pesaje-create'),
    path('detail/<pk>/', views.PesajeDetailView.as_view(), name='pesaje-detail'),
    path('delete/<pk>/', views.PesajeDeleteView.as_view(), name='pesaje-delete'),
    path('edit/<pk>/', views.PesajeEditView.as_view(), name='pesaje-edit'),
    path('list/', views.PesajeListView.as_view(), name='pesaje-list'),
    path('list/search/', views.PesajeSearchListView.as_view(),
         name='pesaje-search-list'),
    path('resporte/pesaje-bruto/<pk>/',
         views.PesajeReporteBrutoView.as_view(), name='reporte-pesaje-bruto'),
    path('resporte/pesaje-neto/<pk>/',
         views.PesajeReporteNetoView.as_view(), name='reporte-pesaje-neto'),
    path('buscar-tara/', views.PesajeBuscarTara.as_view(), name='buscar-tara'),
]
