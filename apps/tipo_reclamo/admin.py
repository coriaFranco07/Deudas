from django.contrib import admin
from .models import TipoReclamo, HistTipoReclamo

# Register your models here.
admin.site.register([TipoReclamo, HistTipoReclamo])
