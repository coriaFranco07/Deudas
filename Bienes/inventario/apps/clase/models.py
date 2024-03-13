from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils.text import slugify  #genera un slug a partir de una cadena de texto
from inventario.util import unique_slug_generator

# Create your models here.

class Clase(models.Model):
    id_clase=models.AutoField(primary_key=True)
    dsc_clase=models.CharField(max_length=30, unique=True)
    fch_user=models.DateTimeField(auto_now=True)
    user_clase=models.ForeignKey(User, on_delete=models.RESTRICT, default=None)
    slug=models.SlugField(max_length=200, null=True,blank=True)
    
    class Meta:
        verbose_name='Clase'
        verbose_name_plural='Clases'
        ordering =['dsc_clase']
        
    def __str__(self) -> str:
        return self.dsc_clase
    
   
    
def slug_generator(sender, instance, *args, **kwargs):
        if not instance.slug:
            
            val=unique_slug_generator(instance)
            instance.slug=slugify(val)
            
pre_save.connect(slug_generator, sender=Clase)
    
    
