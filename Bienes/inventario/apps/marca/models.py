from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils.text import slugify  #genera un slug a partir de una cadena de texto
from inventario.util import unique_slug_generator



# Create your models here.

class Marca(models.Model):
    id_marca=models.AutoField(primary_key=True)
    dsc_marca=models.CharField(max_length=50, unique=True)
    fch_marca=models.DateTimeField(auto_now=True)
    user_marca=models.ForeignKey(User, on_delete=models.RESTRICT, default=None)
    slug=models.SlugField(max_length=200, null=True,blank=True)
    
    class Meta:
        verbose_name='Marca'
        verbose_name_plural='Marcas'
        ordering=['dsc_marca']

    def __str__(self) -> str:
        return self.dsc_marca
    
    """def clean(self) -> None: 
            buscar=Marca.objects.filter(dsc_marca__iexact=self.dsc_marca)
            
            if self.id_marca:
                print('la marca viene de editar')
                buscar = buscar.exclude(pk=self.id_marca)  
            if buscar.exists(): 
                    print('++++++++++++++++++++++++++++++++++++++')    
                    raise ValueError('La Marca Existe en el Modelo')  
            return super().clean()"""
    
def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        
        val=unique_slug_generator(instance)
        instance.slug=slugify(val)
        
pre_save.connect(slug_generator, sender=Marca)