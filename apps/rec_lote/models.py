from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify  #genera un slug a partir de una cadena de texto
from regunicopago.util import unique_slug_generator
from apps.lote.models import Lote
from apps.reclamo.models import Reclamo

# Create your models here.

class Rec_Lote(models.Model):
    id_lote_rec=models.AutoField(primary_key=True)
    id_lote=models.ForeignKey(Lote, on_delete=models.CASCADE)
    id_rec=models.ForeignKey(Reclamo, on_delete=models.RESTRICT, related_name='lotes_reclamos')
    fch_rec_lote=models.DateTimeField(auto_now=True)
    user_rec_lote=models.ForeignKey(User, on_delete=models.RESTRICT)
    slug=models.SlugField(max_length=200, null=True,blank=True)
    
    
    
    
    class Meta:
        verbose_name='Reclamo en lote'
        verbose_name_plural='Reclamos en Lotes'
        ordering=['id_rec']
        unique_together = ('id_rec', 'id_lote')

    def __str__(self) -> str:
       return f" {self.id_rec} - [{self.id_rec.id_tipo_rec.dsc_tipo_rec}] "
    
  
def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        
        val=unique_slug_generator(instance)
        instance.slug=slugify(val)
        
pre_save.connect(slug_generator, sender=Rec_Lote)