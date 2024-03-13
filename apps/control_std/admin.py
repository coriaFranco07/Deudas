from django.contrib import admin
from .models import ControlEstado, HistControlEstado
# Register your models here.
admin.site.register([ControlEstado, HistControlEstado])

