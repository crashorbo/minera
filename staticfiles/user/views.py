from django.shortcuts import render
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from .forms import CustomUserCreationForm
# Create your views here.


class CreateUserView(LoginRequiredMixin, FormView):
    form_class = CustomUserCreationForm
    template_name = "user/create.html"

    def form_valid(self, form):
        form.save()
        return JsonResponse({"message": "usuario registrado con exito"}, status=200)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"message": errors}, status=400)
