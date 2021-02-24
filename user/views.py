from django.forms.forms import Form
from django.shortcuts import render
from django.views.generic import FormView, TemplateView, ListView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db.models import Q
from django.views.generic.edit import DeleteView
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.urls import reverse

from .forms import ColorEditForm, ColorForm, CotizacionForm, CustomUserCreationForm, CustomUserEditForm, CustomUserUpdateForm, DestinoCreateForm
from .models import Cotizacion, CustomUser, Parametro, Destino
# Create your views here.


class ConfiguracionView(LoginRequiredMixin, TemplateView):
    template_name = 'configuracion/index.html'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    # fields = ['username', 'first_name', 'last_name',
    #           'email', 'photo', 'telefono']
    template_name = 'user/profile.html'

    def form_valid(self, form):
        form.save()
        return JsonResponse({"message": "Perfil actualizado con exito"}, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)


class UserListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'user/list.html'


class CreateUserView(LoginRequiredMixin, FormView):
    form_class = CustomUserCreationForm
    template_name = 'user/create.html'

    def form_valid(self, form):
        form.save()
        return JsonResponse({"message": "Usuario registrado con exito"}, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)


class UserEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserEditForm
    template_name = 'user/edit.html'

    def form_valid(self, form):
        form.save()
        return JsonResponse({"message": "Informacion de Usuario editado con exito"}, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)


class ParametroView(LoginRequiredMixin, TemplateView):
    template_name = 'parametro/index.html'


class CotizacionCreateView(LoginRequiredMixin, FormView):
    form_class = CotizacionForm
    template_name = 'cotizacion/create.html'

    def form_valid(self, form):
        form.save()
        return JsonResponse({"message": "Cotizacion registrada con exito"}, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)


class CotizacionUpdateView(LoginRequiredMixin, UpdateView):
    model = Cotizacion
    form_class = CotizacionForm
    template_name = 'cotizacion/edit.html'

    def form_valid(self, form):
        form.save()
        return JsonResponse({"message": "Cotizacion Editado con exito"}, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)


class CotizacionDeleteView(LoginRequiredMixin, DeleteView):
    model = Cotizacion
    template_name = 'cotizacion/delete.html'

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        return JsonResponse({"message": "Cotizacion Eliminada con exito"}, status=200)


class CotizacionListJson(LoginRequiredMixin, BaseDatatableView):
    model = Cotizacion
    columns = ['fecha_inicio', 'fecha_fin', 'valor']

    # define column names that will be used in sorting
    # order is important and should be same as order of columns
    # displayed by datatables. For non sortable columns use empty
    # value like ''
    order_columns = ['fecha_inicio', 'fecha_fin', 'valor']

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 50

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'user':
            # escape HTML for security reasons
            return escape('{0} {1}'.format(row.customer_firstname, row.customer_lastname))
        else:
            return super(CotizacionListJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        # use parameters passed in GET request to filter queryset

        # simple example:
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(valor__icontains=search)

        # more advanced example using extra parameters
        filter_customer = self.request.GET.get('customer', None)

        if filter_customer:
            customer_parts = filter_customer.split(' ')
            qs_params = None
            for part in customer_parts:
                q = Q(customer_firstname__istartswith=part) | Q(
                    customer_lastname__istartswith=part)
                qs_params = qs_params | q if qs_params else q
            qs = qs.filter(qs_params)
        return qs

    def prepare_results(self, qs):
        # prepare list with output column data
        # queryset is already paginated here
        json_data = []
        for item in qs:
            json_data.append([
                # escape HTML for security reasons
                escape(item.fecha_inicio.strftime("%d/%m/%Y")),
                # escape HTML for security reasons
                escape(item.fecha_fin.strftime("%d/%m/%Y")),
                escape(item.valor),
                '<div class="text-end cotizacion-options"><i data-url="{}" class="bi bi-pencil-square"></i><i data-url="{}" class="bi bi-trash ms-2"></i></div>'.format(
                    reverse('cotizacion-edit', kwargs={'pk': item.id}), reverse('cotizacion-delete', kwargs={'pk': item.id}))
            ])
        return json_data


class ColorListView(LoginRequiredMixin, ListView):
    model = Parametro
    template_name = 'color/list.html'

    def get_queryset(self):
        return Parametro.objects.filter(tipo=0)


class ColorCreateView(LoginRequiredMixin, FormView):
    form_class = ColorForm
    template_name = 'color/create.html'

    def form_valid(self, form):
        form.save()
        return JsonResponse({"message": "Color registrado con exito"}, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)


class ColorUpdateView(LoginRequiredMixin, UpdateView):
    model = Parametro
    form_class = ColorEditForm
    template_name = 'color/edit.html'

    def form_valid(self, form):
        form.save()
        return JsonResponse({"message": "Color Editado con exito"}, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)


class DestinoListView(LoginRequiredMixin, ListView):
    model = Destino
    template_name = 'destino/list.html'


class DestinoCreateView(LoginRequiredMixin, FormView):
    form_class = DestinoCreateForm
    template_name = 'destino/create.html'

    def form_valid(self, form):
        form.save()
        return JsonResponse({"message": "Destino registrado con exito"}, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)


class DestinoUpdateView(LoginRequiredMixin, UpdateView):
    model = Destino
    form_class = DestinoCreateForm
    template_name = 'destino/edit.html'

    def form_valid(self, form):
        form.save()
        return JsonResponse({"message": "Destino editado con exito"}, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)
