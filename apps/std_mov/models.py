from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils.text import slugify  #genera un slug a partir de una cadena de texto
from regunicopago.util import unique_slug_generator

# Create your models here.

class EstadoMov(models.Model):
    id_std_mov=models.AutoField(primary_key=True)
    dsc_std_mov=models.CharField(max_length=50, unique=True)
    fch_std_mov=models.DateTimeField(auto_now=True)
    user_std_mov=models.ForeignKey(User, on_delete=models.RESTRICT)
    slug=models.SlugField(max_length=200, null=True,blank=True)
    
    
    
    
    class Meta:
        verbose_name='Estado de Movimiento'
        verbose_name_plural='Estados de Movimientos'
        ordering=['dsc_std_mov']
        

    def __str__(self) -> str:
       return f" {self.id_std_mov}:  {self.dsc_std_mov} "
    
  
def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        
        val=unique_slug_generator(instance)
        instance.slug=slugify(val)
        
pre_save.connect(slug_generator, sender=EstadoMov)


class HistEstadoMov(models.Model):
    h_id_std_mov=models.AutoField(primary_key=True)
    id_std_mov=models.PositiveIntegerField()
    dsc_std_mov=models.CharField(max_length=50)
    fch_std_mov=models.DateTimeField(auto_now=True)
    user_std_mov=models.CharField(max_length=20)
    slug=models.CharField(max_length=200, null=True,blank=True)
    h_user_proc=models.ForeignKey(User, on_delete=models.RESTRICT)
    h_fch_proc=models.DateTimeField(auto_now_add=True)
    h_tipo_proc = models.CharField(max_length=1, null=True)
   
    
    
    
    
    class Meta:
        verbose_name='H_Estado de Movimiento'
        verbose_name_plural='H_Estados de Movimientos'
        ordering=['-h_fch_proc']
        

    def __str__(self) -> str:
       return f"{self.dsc_std_mov} : {self.h_fch_proc} : {self.h_user_proc} : {self.h_tipo_proc} "