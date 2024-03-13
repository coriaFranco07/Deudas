from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify  #genera un slug a partir de una cadena de texto
from regunicopago.util import unique_slug_generator
from apps.tipo_reclamo.models import TipoReclamo

# Create your models here.

class Legajo(models.Model):
    id_legajo=models.AutoField(primary_key=True)
    nro_doc=models.PositiveBigIntegerField(unique=True)
    nombres=models.CharField(blank=False, null=False,max_length=200)
    jerarquia=models.CharField(blank=True, null=True,max_length=100)
    cuerpo=models.CharField(blank=True, null=True,max_length=50)
    fch_leg=models.DateTimeField(auto_now=True)
    user_leg=models.ForeignKey(User, on_delete=models.RESTRICT)
    slug=models.SlugField(max_length=200, null=True,blank=True)
    
    
    
    
    class Meta:
        verbose_name='Legajo'
        verbose_name_plural='Legajos'
        ordering=['nro_doc']

    def __str__(self) -> str:
       return f" {self.nro_doc} : {self.nombres}  "
    
  
def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        
        val=unique_slug_generator(instance)
        instance.slug=slugify(val)
        
pre_save.connect(slug_generator, sender=Legajo)

class HistLegajo(models.Model):
    h_id_legajo=models.AutoField(primary_key=True)
    id_legajo=models.PositiveBigIntegerField()
    nro_doc=models.PositiveBigIntegerField()
    nombres=models.CharField(blank=False, null=False,max_length=200)
    jerarquia=models.CharField(blank=True, null=True,max_length=100)
    cuerpo=models.CharField(blank=True, null=True,max_length=50)
    fch_leg=models.DateTimeField(auto_now=True)
    user_leg=models.CharField(max_length=20)
    slug=models.CharField(max_length=200, null=True,blank=True)
    
    h_user_proc=models.ForeignKey(User, on_delete=models.RESTRICT)
    h_fch_proc=models.DateTimeField(auto_now_add=True)
    h_tipo_proc = models.CharField(max_length=1, null=True)
    
    
    
    
    class Meta:
        verbose_name='H_Legajo'
        verbose_name_plural='H_Legajos'
        ordering=['-h_fch_proc']

    def __str__(self) -> str:
       return f" {self.nro_doc} [{self.nombres} {self.jerarquia} {self.cuerpo}] -  {self.h_fch_proc} : {self.h_user_proc} : {self.h_tipo_proc} "