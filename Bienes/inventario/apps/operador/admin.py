from django.contrib import admin
from .models import Operador

# Register your models here.
class OperardorAdmin(admin.ModelAdmin):
      list_display = ('operador', 'oficina','slug') #Ahora la interfaz mostrará nombre, apellido y email de cada autor.
      search_fields = ('operador', 'oficina')
admin.site.register(Operador, OperardorAdmin)
