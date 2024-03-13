import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils.text import slugify  #genera un slug a partir de una cadena de texto
from inventario.util import unique_slug_generator
from apps.clase.models import Clase
from apps.tipo.models import Tipo
from apps.marca.models import Marca
from apps.modelo.models import Modelo



# Create your models here.

class Bien(models.Model):
    id_bien=models.AutoField(primary_key=True)
    clase=models.ForeignKey(Clase, on_delete=models.RESTRICT, blank=True, related_name='clase')
    tipo=models.ForeignKey(Tipo, on_delete=models.RESTRICT, blank=True, related_name='tipo')
    marca=models.ForeignKey(Marca, on_delete=models.RESTRICT, blank=True, related_name='marca')
    modelo=models.ForeignKey(Modelo, on_delete=models.RESTRICT, blank=True, related_name='modelo')
    cupi=models.PositiveIntegerField(unique=True, default=0)
    no_inventariado=models.BooleanField(default=False, null=False, blank=False)
    serie=models.CharField(max_length=200, null=True, blank=True, default='S/N')
    nro_inventario= models.CharField(max_length=50,null=True, blank=True, default=0)
    qr_bien=models.TextField(null=True, blank=True)
    obs_bien=models.CharField(max_length=300, null=True, blank=True)
    gde_bien=models.CharField(max_length=80, null=True, blank=True)
    user_bien=models.ForeignKey(User, on_delete=models.PROTECT)
    fch_bien=models.DateTimeField(auto_now=True)
    slug=models.SlugField(max_length=200, null=True,blank=True)
   
    
    class Meta:
        verbose_name='Bien'
        verbose_name_plural='Bienes'
        ordering=['tipo']

    def __str__(self) -> str:
        return f" ({self.cupi})-{self.tipo} -{self.marca} - {self.modelo} - {self.serie} "
    
    def clean(self) -> None: 
            buscar=Bien.objects.filter(cupi__iexact=self.cupi)
            
            if self.id_bien:
                buscar = buscar.exclude(pk=self.id_bien)  
            if buscar.exists():     
                    raise ValueError('El Nro. de Cupi Existe')  
            return super().clean()




    
def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        
        val=unique_slug_generator(instance)
        instance.slug=slugify(val)
        
pre_save.connect(slug_generator, sender=Bien)