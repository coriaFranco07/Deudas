from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils.text import slugify  #genera un slug a partir de una cadena de texto
from regunicopago.util import unique_slug_generator
from django.core.validators import MinValueValidator

# Create your models here.

class TipoReclamo(models.Model):
    id_tipo_rec=models.AutoField(primary_key=True)
    codigo_rec = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    dsc_tipo_rec=models.CharField(max_length=50, unique=True)
    tipo_anual=models.BooleanField(default=False)
    fch_tipo_rec=models.DateTimeField(auto_now=True)
    user_tipo_rec=models.ForeignKey(User, on_delete=models.RESTRICT)
    slug=models.SlugField(max_length=200, null=True,blank=True)
   
    
    class Meta:
        verbose_name='Tipo Reclamo'
        verbose_name_plural='Tipos Reclamos'
        ordering=['dsc_tipo_rec']

    def __str__(self) -> str:
        return  f" ({self.codigo_rec}) - {self.dsc_tipo_rec}"
    
  
def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        
        val=unique_slug_generator(instance)
        instance.slug=slugify(val)
        
pre_save.connect(slug_generator, sender=TipoReclamo)



class HistTipoReclamo(models.Model):
    h_id_tipo_rec=models.AutoField(primary_key=True)
    id_tipo_rec=models.PositiveIntegerField()
    codigo_rec = models.PositiveSmallIntegerField()
    dsc_tipo_rec=models.CharField(max_length=50)
    tipo_anual=models.BooleanField(default=False)
    fch_tipo_rec=models.DateTimeField(auto_now=True)
    user_tipo_rec=models.CharField(max_length=20)
    slug=models.CharField(max_length=200, null=True,blank=True)
    h_user_proc=models.ForeignKey(User, on_delete=models.RESTRICT)
    h_fch_proc=models.DateTimeField(auto_now_add=True)
    h_tipo_proc = models.CharField(max_length=1, null=True)
   
    
    class Meta:
        verbose_name='H_Tipo Reclamo'
        verbose_name_plural='H_Tipos Reclamos'
        ordering=['-h_fch_proc']

    def __str__(self) -> str:
        return f"{self.codigo_rec} - {self.dsc_tipo_rec} - {self.tipo_anual}: {self.h_fch_proc} : {self.h_user_proc} : {self.h_tipo_proc} "