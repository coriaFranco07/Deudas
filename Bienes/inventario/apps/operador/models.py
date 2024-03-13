from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils.text import slugify  #genera un slug a partir de una cadena de texto
from inventario.util import unique_slug_generator
from apps.oficina.models import Oficina



# Create your models here.

class Operador(models.Model):
    operador=models.OneToOneField(User, to_field='id', primary_key=True, on_delete=models.RESTRICT, related_name='operador')
    oficina=models.ForeignKey(Oficina,  on_delete=models.RESTRICT, name='oficina')
    fch_operador=models.DateTimeField(auto_now=True)
    user_operador=models.ForeignKey(User, to_field='id' ,on_delete=models.RESTRICT, related_name='operador_oficina',default=None)
    slug=models.SlugField(max_length=200, null=True,blank=True)
    
    class Meta:
        verbose_name='Operador'
        verbose_name_plural='Operadores'
        ordering=['operador']

    def __str__(self) -> str:
        return f'{self.operador}-{self.oficina}'
    
def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        
        val=unique_slug_generator(instance)
        instance.slug=slugify(val)
        
pre_save.connect(slug_generator, sender=Operador)