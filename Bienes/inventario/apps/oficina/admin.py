from django.contrib import admin
from .models import Oficina

class OficinaAdmin(admin.ModelAdmin):
    search_fields=['dsc_oficina']
    ordering=['dsc_oficina']
    autocomplete_fields=['id_oficina_padre']

# Register your models here.
admin.site.register(Oficina, OficinaAdmin)
