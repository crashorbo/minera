from django.urls import path

from . import views

urlpatterns = [
    path('', views.PesajeList.as_view(), name='pesaje-list'),
]
