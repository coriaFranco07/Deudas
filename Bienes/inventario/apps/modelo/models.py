from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils.text import slugify  #genera un slug a partir de una cadena de texto
from inventario.util import unique_slug_generator


# Create your models here.

class Modelo(models.Model):
    id_modelo=models.AutoField(primary_key=True)
    dsc_modelo=models.CharField(max_length=30, unique=True)
    fch_modelo=models.DateTimeField(auto_now=True)
    user_modelo=models.ForeignKey(User, on_delete=models.RESTRICT, default=None)
    slug=models.SlugField(max_length=200, null=True,blank=True)
    
    class Meta:
        verbose_name='Modelo'
        verbose_name_plural='Modelos'
        ordering =['dsc_modelo']
        
    def __str__(self) -> str:
        return self.dsc_modelo
    
    """def clean(self) -> None:
            buscar=Modelo.objects.filter(dsc_modelo__iexact=self.dsc_modelo)
            
            if self.id_modelo:
                buscar = buscar.exclude(pk=self.id_modelo)  
            if buscar.exists():     
                    raise ValueError('El Modelo Existe')  
            return super().clean()"""

def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        
        val=unique_slug_generator(instance)
        instance.slug=slugify(val)
        
pre_save.connect(slug_generator, sender=Modelo)