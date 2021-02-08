import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
TIPO_ROL = (
    (0, 'Gerente'),
    (1, 'Administracion'),
    (2, 'Pesaje'),
    (3, 'Laboratorio'),
    (4, 'Contabilidad'),
)


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    photo = models.ImageField(
        upload_to='users/avatars/', null=True, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    rol = models.IntegerField(choices=TIPO_ROL, default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)
