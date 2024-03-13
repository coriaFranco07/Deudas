from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils.text import slugify  #genera un slug a partir de una cadena de texto
from inventario.util import unique_slug_generator



# Create your models here.

class Estado(models.Model):
    id_estado=models.AutoField(primary_key=True)
    dsc_estado=models.CharField(max_length=30, unique=True)
    origen=models.BooleanField(default=True)
    fch_estado=models.DateTimeField(auto_now=True)
    user_estado=models.ForeignKey(User, on_delete=models.RESTRICT, default=None)
    slug=models.SlugField(max_length=200, null=True,blank=True)
    
    class Meta:
        verbose_name='Estado'
        verbose_name_plural='Estados'
        ordering=['dsc_estado']

    def __str__(self) -> str:
        return self.dsc_estado
    
    """def clean(self) -> None: 
            buscar=Estado.objects.filter(dsc_estado__iexact=self.dsc_estado)
           
            if self.id_estado:
                buscar = buscar.exclude(pk=self.id_estado)  
            if buscar.exists():     
                    raise ValueError('El Estado Existe')  
            return super().clean()"""
    
def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        
        val=unique_slug_generator(instance)
        instance.slug=slugify(val)
        
pre_save.connect(slug_generator, sender=Estado)