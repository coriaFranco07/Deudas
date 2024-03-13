from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify  #genera un slug a partir de una cadena de texto
from regunicopago.util import unique_slug_generator

# Create your models here.

class Lote(models.Model):
    id_lote=models.AutoField(primary_key=True)
    nivel_lote=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(12)], default=1)
    year_lote=models.PositiveIntegerField(validators=[MinValueValidator(2023),MaxValueValidator(2050)])
    activo_lote=models.BooleanField(default=True)
    importe_lote=models.FloatField(default=0)
    saldo_lote=models.FloatField(default=0)
    fch_lote=models.DateTimeField(auto_now=True)
    user_lote=models.ForeignKey(User, on_delete=models.RESTRICT)
    slug=models.SlugField(max_length=200, null=True,blank=True)
   
    
    class Meta:
        verbose_name='Lote'
        verbose_name_plural='Lotes'
        ordering=['-year_lote','nivel_lote']
        unique_together = ('nivel_lote','year_lote')

    def __str__(self) -> str:
       return f" {self.id_lote} - [{self.year_lote} - {self.nivel_lote}] -  [IMP: ${self.importe_lote} - SALDO: ${self.saldo_lote}] -(Activo:{self.activo_lote})"
    
  
def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        
        val=unique_slug_generator(instance)
        instance.slug=slugify(val)
        
pre_save.connect(slug_generator, sender=Lote)


class HistLote(models.Model):
    h_id_lote=models.AutoField(primary_key=True)
    id_lote=models.PositiveIntegerField()
    nivel_lote=models.PositiveIntegerField()
    year_lote=models.PositiveIntegerField()
    activo_lote=models.BooleanField(default=True)
    importe_lote=models.FloatField(default=0)
    saldo_lote=models.FloatField(default=0)
    fch_lote=models.DateTimeField(auto_now=True)
    user_lote=models.CharField(max_length=20)
    slug=models.CharField(max_length=200, null=True,blank=True)
    h_user_proc=models.ForeignKey(User, on_delete=models.RESTRICT)
    h_fch_proc=models.DateTimeField(auto_now_add=True)
    h_tipo_proc = models.CharField(max_length=1, null=True)
   
    
    class Meta:
        verbose_name='H_Lote'
        verbose_name_plural='H_Lotes'
        ordering=['-h_fch_proc']
        

    def __str__(self) -> str:
        return f"{self.year_lote} - {self.nivel_lote}: {self.h_fch_proc} : {self.h_user_proc} : {self.h_tipo_proc} "