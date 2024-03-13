from django.contrib import admin
from .models import Legajo, HistLegajo
# Register your models here.
admin.site.register([Legajo, HistLegajo])
