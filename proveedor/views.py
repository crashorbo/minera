from django.shortcuts import render
from django.views.generic import TemplateView, FormView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeleteView
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.urls import reverse
from django.db.models import Q
from django.http.response import JsonResponse

from .models import Proveedor
from .forms import ProovedorCreateForm

from pesaje.models import Carga
# Create your views here.


class ProveedorTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'proveedor/index.html'


class ProveedorListJson(LoginRequiredMixin, BaseDatatableView):
    model = Proveedor
    columns = ['apellidos', 'nombres',
               'numero_documento', 'telefono', 'direccion']

    # define column names that will be used in sorting
    # order is important and should be same as order of columns
    # displayed by datatables. For non sortable columns use empty
    # value like ''
    order_columns = ['apellidos', 'nombres',
                     'numero_documento', 'telefono', 'direccion']

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 50

    def get_initial_queryset(self):
        # return queryset used as base for futher sorting/filtering
        # these are simply objects displayed in datatable
        # You should not filter data returned here by any filter values entered by user. This is because
        # we need some base queryset to count total number of records.
        return Proveedor.objects.filter(deleted=False)

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'nombre':
            # escape HTML for security reasons
            return escape('{0} {1}'.format(row.nombres, row.apellidos))
        else:
            return super(ProveedorListJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        # use parameters passed in GET request to filter queryset

        # simple example:
        search = self.request.GET.get('search[value]', None)
        if search:
            q_search = Q(nombres__contains=search) | Q(apellidos__contains=search) | Q(
                numero_documento__contains=search) | Q(telefono__contains=search) | Q(direccion__contains=search)
            qs = qs.filter(q_search)
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
                '{} {}'.format(item.apellidos, item.nombres),
                item.numero_documento,
                # escape HTML for security reasons
                escape(item.telefono) if item.telefono else '',
                escape(item.direccion) if item.direccion else '',
                '<div class="text-end cotizacion-options"><i data-url="{}" class="bi bi-pencil-square"></i><i data-url="{}" class="bi bi-trash ms-2"></i>'.format(
                    reverse('proveedor-edit', kwargs={'pk': item.id}), reverse('proveedor-delete', kwargs={'pk': item.id}))
            ])
        return json_data


class ProveedorCreateView(LoginRequiredMixin, FormView):
    form_class = ProovedorCreateForm
    template_name = 'proveedor/create.html'

    def form_valid(self, form):
        form.save()
        return JsonResponse({"message": "Proveedor registrado con exito"}, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)


class ProveedorEditView(LoginRequiredMixin, UpdateView):
    model = Proveedor
    form_class = ProovedorCreateForm
    template_name = 'proveedor/edit.html'

    def form_valid(self, form):
        form.save()
        return JsonResponse({"message": "Datos de Proveedor editado con exito"}, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)


class ProveedorDeleteView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        proveedor = Proveedor.objects.get(id=kwargs['pk'])
        return render(self.request, 'proveedor/delete.html', {'proveedor': proveedor})

    def post(self, *args, **kwargs):
        proveedor = Proveedor.objects.get(id=kwargs['pk'])
        pesajes = Carga.objects.filter(proveedor=proveedor.id)
        if pesajes:
            proveedor.deleted = True
            proveedor.save()
            return JsonResponse({"message": "Se ha dado de baja al proveedor con exito"}, status=200)
        proveedor.delete()
        return JsonResponse({"message": "Se ha eliminado al proveedor con exito"}, status=200)


class ProveedorAutocomplete(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        q = self.request.GET['q']
        object_list = Proveedor.objects.filter(deleted=False)
        filtered_object_list = object_list
        if len(q) > 0:
            filtered_object_list = object_list.filter_on_search(q)
        qs = filtered_object_list
        qs = self.get_results(qs)
        return JsonResponse({
            'results': qs
        }, content_type='application/json')

    def get_results(self, results):
        return [dict(id=x.id, text='{} - {} {}'.format(x.numero_documento, x.apellidos, x.nombres)) for x in results]
