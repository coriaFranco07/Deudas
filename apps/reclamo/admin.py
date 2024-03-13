from django.contrib import admin
from .models import Reclamo, HistReclamo
# Register your models here.
admin.site.register([Reclamo, HistReclamo])
