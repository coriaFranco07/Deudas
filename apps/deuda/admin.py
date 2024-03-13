from django.contrib import admin
from .models import Deuda, HistDeuda
# Register your models here.
admin.site.register([Deuda, HistDeuda])
