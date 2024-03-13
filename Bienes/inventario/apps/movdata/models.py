from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils.text import slugify  #genera un slug a partir de una cadena de texto
from inventario.util import unique_slug_generator
from apps.bien.models import Bien
from apps.estado.models import Estado
from apps.oficina.models import Oficina
from django.contrib.contenttypes.fields import GenericRelation



# Create your models here.

class MovData(models.Model):
    id_mov=models.AutoField(primary_key=True)
    bien_mov=models.ForeignKey(Bien, on_delete=models.RESTRICT, related_name='movimientos',blank=True)
    estado=models.ForeignKey(Estado, on_delete=models.RESTRICT, default='Alta', related_name='estado')
    origen=models.ForeignKey(Oficina ,to_field='id_oficina' ,on_delete=models.RESTRICT, related_name='oficina', default=None)
    gde_mov=models.CharField(max_length=80, blank=True, null=True)
    observ_mov=models.TextField(max_length=500, blank=True, null=True)
    fch_dsd=models.DateTimeField(auto_now_add=True, auto_now=False)
    fch_hst=models.DateTimeField(blank=True, null=True)
    destino=models.ForeignKey(Oficina ,to_field='id_oficina',on_delete=models.RESTRICT, related_name='destino', default=None)
    user_mov=models.ForeignKey(User, on_delete=models.RESTRICT, default=None)
    slug=models.SlugField(max_length=200, null=True,blank=True)
    
    
    class Meta:
        verbose_name='MovData'
        verbose_name_plural='MovDatas'
        ordering=['bien_mov']

    def __str__(self) -> str:
        return f'{self.bien_mov.cupi} - {self.destino}'
    
def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        
        val=unique_slug_generator(instance)
        instance.slug=slugify(val)
        
#def destinos(self):
#    return Oficina.objects.all()
pre_save.connect(slug_generator, sender=MovData)