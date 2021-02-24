from django.urls import path
from django.conf.urls import url

from .views import VehiculoTemplateView, VehiculoListJson, VehiculoCreateView, VehiculoEditView

urlpatterns = [
    path('', VehiculoTemplateView.as_view(), name='vehiculo-list'),
    url(r'^list/json/$',
        VehiculoListJson.as_view(), name='conductor-json'),
    path('create/', VehiculoCreateView.as_view(), name='vehiculo-create'),
    path('edit/<pk>/', VehiculoEditView.as_view(), name='vehiculo-edit'),
]
