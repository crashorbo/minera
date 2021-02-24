from django.urls import path
from django.conf.urls import url

from .views import ColorCreateView, ColorListView, ColorUpdateView, CotizacionDeleteView, CotizacionListJson, CotizacionUpdateView, CreateUserView, ParametroView, ProfileUpdateView, ConfiguracionView, UserEditView, UserListView, CotizacionCreateView, \
    DestinoCreateView, DestinoListView, DestinoUpdateView

urlpatterns = [
    path('configuracion/', ConfiguracionView.as_view(), name='user-configuracion'),
    path('create/', CreateUserView.as_view(), name='user-create'),
    path('list/', UserListView.as_view(), name='user-list'),
    path('profile/<pk>/', ProfileUpdateView.as_view(), name='user-profile'),
    path('edit/<pk>/', UserEditView.as_view(), name='user-edit'),
    path('parametro/', ParametroView.as_view(), name='parametro-index'),
    path('parametro/cotizacion/create/',
         CotizacionCreateView.as_view(), name='cotizacion-create'),
    path('parametro/cotizacion/edit/<pk>/',
         CotizacionUpdateView.as_view(), name='cotizacion-edit'),
    path('parametro/cotizacion/delete/<pk>/',
         CotizacionDeleteView.as_view(), name='cotizacion-delete'),
    url(r'^parametro/cotizacion/json/$',
        CotizacionListJson.as_view(), name='cotizacion-json'),
    path('parametro/color/list/',
         ColorListView.as_view(), name='color-list'),
    path('parametro/color/create/',
         ColorCreateView.as_view(), name='color-create'),
    path('parametro/color/edit/<pk>/',
         ColorUpdateView.as_view(), name='color-edit'),
    path('parametro/destino/list/',
         DestinoListView.as_view(), name='destino-list'),
    path('parametro/destino/create/',
         DestinoCreateView.as_view(), name='destino-create'),
    path('parametro/destino/edit/<pk>/',
         DestinoUpdateView.as_view(), name='destino-edit'),
]
