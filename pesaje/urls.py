from django.urls import path

from . import views

urlpatterns = [
    path('', views.PesajeListView.as_view(), name='pesaje-list'),
    path('create/', views.PesajeCreateView.as_view(), name='pesaje-create'),
]
