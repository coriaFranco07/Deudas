from django.contrib import admin
from .models import EstadoMov, HistEstadoMov
# Register your models here.
admin.site.register([EstadoMov, HistEstadoMov])
