from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils.text import slugify  #genera un slug a partir de una cadena de texto
from inventario.util import unique_slug_generator

# Create your models here.

class Tipo(models.Model):
    id_tipo=models.AutoField(primary_key=True)
    dsc_tipo=models.CharField(max_length=30, unique=True)
    fch_tipo=models.DateTimeField(auto_now=True)
    user_tipo=models.ForeignKey(User, on_delete=models.RESTRICT, default=None)
    slug=models.SlugField(max_length=200, null=True,blank=True)
    
    class Meta:
        verbose_name='tipo'
        verbose_name_plural='tipo'
        ordering=['dsc_tipo']

    def __str__(self) -> str:
        return self.dsc_tipo
    
    """def clean(self) -> None: 
            buscar=Tipo.objects.filter(dsc_tipo__iexact=self.dsc_tipo)
            
            if self.id_tipo:
                buscar = buscar.exclude(pk=self.id_tipo)  
            if buscar.exists():     
                    raise ValueError('El Tipo de Bien Existe')  
            return super().clean()
    """
def slug_generator(sender, instance, *args, **kwargs):
        if not instance.slug:
            
            val=unique_slug_generator(instance)
            instance.slug=slugify(val)
            
pre_save.connect(slug_generator, sender=Tipo)  