from django.contrib import admin
from .models import Bien
from apps.imgbien.models import ImgBien
from .forms import BienForm



# Register your models here.

class ImgBienAdmin(admin.TabularInline):
    model=ImgBien
    
class BienAdmin(admin.ModelAdmin):
    form=BienForm
    inlines=[
        ImgBienAdmin
    ]


admin.site.register(Bien, BienAdmin)

