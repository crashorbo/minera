from django.urls import path

from . import views

urlpatterns = [
    path('', views.PesajeIndexView.as_view(), name='pesaje-index'),
    path('create/', views.PesajeCreateView.as_view(), name='pesaje-create'),
    path('list/', views.PesajeListView.as_view(), name='pesaje-list'),
]
