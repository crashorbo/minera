from django.urls import path
from django.conf.urls import url

from django.contrib.auth import views as auth_views

from .views import CotizacionDeleteView, CotizacionListJson, CotizacionUpdateView, CreateUserView, ParametroView, ProfileUpdateView, ConfiguracionView, UserEditView, UserListView, CotizacionCreateView, \
    DestinoCreateView, DestinoListView, DestinoUpdateView, LaboratorioListView, LaboratorioCreateView, LaboratorioUpdateView, GeneradorListJson, GeneradorCreateView, GeneradorPrintView, \
    UbicacionView, LaboratorioView, OrigenListView, OrigenCreateView, OrigenUpdateView, CodigoAutoComplete, FactorCreateView, FactorListView, FactorUpdateView

urlpatterns = [
    path('configuracion/', ConfiguracionView.as_view(), name='user-configuracion'),
    path('create/', CreateUserView.as_view(), name='user-create'),
    path('list/', UserListView.as_view(), name='user-list'),
    path('profile/<pk>/', ProfileUpdateView.as_view(), name='user-profile'),
    path('edit/<pk>/', UserEditView.as_view(), name='user-edit'),
    path('parametro/', ParametroView.as_view(), name='parametro-index'),
    path('parametro/ubicacion/', UbicacionView.as_view(),
         name='parametro-ubicacion-index'),
    path('parametro/laboratorio/', LaboratorioView.as_view(),
         name='parametro-laboratorio-index'),
    path('parametro/cotizacion/create/',
         CotizacionCreateView.as_view(), name='cotizacion-create'),
    path('parametro/cotizacion/edit/<pk>/',
         CotizacionUpdateView.as_view(), name='cotizacion-edit'),
    path('parametro/cotizacion/delete/<pk>/',
         CotizacionDeleteView.as_view(), name='cotizacion-delete'),
    url(r'^parametro/cotizacion/json/$',
        CotizacionListJson.as_view(), name='cotizacion-json'),
    path('parametro/origen/list/',
         OrigenListView.as_view(), name='origen-list'),
    path('parametro/origen/create/',
         OrigenCreateView.as_view(), name='origen-create'),
    path('parametro/origen/edit/<pk>/',
         OrigenUpdateView.as_view(), name='origen-edit'),
    path('parametro/destino/list/',
         DestinoListView.as_view(), name='destino-list'),
    path('parametro/destino/create/',
         DestinoCreateView.as_view(), name='destino-create'),
    path('parametro/destino/edit/<pk>/',
         DestinoUpdateView.as_view(), name='destino-edit'),
    path('parametro/laboratorio/list/',
         LaboratorioListView.as_view(), name='laboratorio-list'),
    path('parametro/laboratorio/create/',
         LaboratorioCreateView.as_view(), name='laboratorio-create'),
    path('parametro/laboratorio/edit/<pk>/',
         LaboratorioUpdateView.as_view(), name='laboratorio-edit'),
    url(r'^parametro/generador/json/$',
        GeneradorListJson.as_view(), name='generador-json'),
    path('parametro/generador/create/',
         GeneradorCreateView.as_view(), name='generador-create'),
    path('parametro/generador/reporte/<pk>/',
         GeneradorPrintView.as_view(), name='generador-reporte'),
    url(r'^codigo-autocomplete/$', CodigoAutoComplete.as_view(),
        name='codigo-autocomplete'),
    path('parametro/factor/create/',
         FactorCreateView.as_view(), name='factor-create'),
    path('parametro/factor/edit/<pk>/',
         FactorUpdateView.as_view(), name='factor-edit'),
    path('parametro/factor/list/',
         FactorListView.as_view(), name='factor-list'),
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='user/change-password.html',
            success_url='/user/logout/'
        ),
        name='change_password_personal'
    ),
]
