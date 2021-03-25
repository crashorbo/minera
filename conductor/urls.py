from django.urls import path
from django.conf.urls import url

from .views import CarguioAutocomplete, VehiculoTemplateView, VehiculoListJson, VehiculoCreateView, VehiculoEditView, VehiculoAutocomplete, ConductorCreateView, \
    ConductorEditView, ConductorListJson, ConductorAutocomplete

urlpatterns = [
    path('', VehiculoTemplateView.as_view(), name='vehiculo-list'),
    url(r'^list/json/$',
        VehiculoListJson.as_view(), name='vehiculo-json'),
    url(r'^vehiculo-autocomplete/$', VehiculoAutocomplete.as_view(),
        name='vehiculo-autocomplete'),
    url(r'^carguio-autocomplete/$', CarguioAutocomplete.as_view(),
        name='carguio-autocomplete'),
    path('create/', VehiculoCreateView.as_view(), name='vehiculo-create'),
    path('edit/<pk>/', VehiculoEditView.as_view(), name='vehiculo-edit'),
    path('conductor/create/', ConductorCreateView.as_view(),
         name='conductor-create'),
    path('conductor/edit/<pk>/', ConductorEditView.as_view(), name='conductor-edit'),
    url(r'^conductor/list/json/$',
        ConductorListJson.as_view(), name='conductor-json'),
    url(r'^conductor-autocomplete/$', ConductorAutocomplete.as_view(),
        name='conductor-autocomplete'),
]
