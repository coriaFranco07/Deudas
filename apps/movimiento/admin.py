from django.contrib import admin
from .models import Movimiento, HistMovimiento
# Register your models here.
admin.site.register([Movimiento, HistMovimiento])
