from django.contrib import admin
from .models import Estado, HistEstado
# Register your models here.
admin.site.register([Estado, HistEstado])
