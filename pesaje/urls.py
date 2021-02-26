from django.urls import path

from . import views

urlpatterns = [
    path('', views.PesajeIndexView.as_view(), name='pesaje-index'),
    path('create/', views.PesajeCreateView.as_view(), name='pesaje-create'),
    path('detail/<pk>', views.PesajeDetailView.as_view(), name='pesaje-detail'),
    path('tara/<pk>/', views.PesajeTaraView.as_view(), name='pesaje-tara'),
    path('list/', views.PesajeListView.as_view(), name='pesaje-list'),
    path('resporte/pesaje/<pk>/',
         views.PesajeReporteView.as_view(), name='pesaje-reporte'),
]
