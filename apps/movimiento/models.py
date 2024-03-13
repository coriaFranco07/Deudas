from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify  #genera un slug a partir de una cadena de texto
from regunicopago.util import unique_slug_generator
from apps.reclamo.models import Reclamo
from apps.std_mov.models import EstadoMov


# Create your models here.

class Movimiento(models.Model):
    id_mov=models.AutoField(primary_key=True)
    fch_mov=models.DateField(blank=False, null=False)
    id_rec=models.ForeignKey(Reclamo, to_field='id_rec',on_delete=models.RESTRICT, related_name='movs_reclamos')
    id_std_mov=models.ForeignKey(EstadoMov, on_delete=models.RESTRICT)
    gde_mov=models.CharField(max_length=50, null=True,blank=True)
    obs_mov=models.CharField(max_length=200, null=True,blank=True)
    fch_std_mov=models.DateField(blank=False, null=False)
    fch_mov_user=models.DateTimeField(auto_now_add=True)
    user_mov=models.ForeignKey(User, on_delete=models.RESTRICT)
    slug=models.SlugField(max_length=200, null=True,blank=True)
    
   
    
    
    class Meta:
        verbose_name='Movimiento'
        verbose_name_plural='Movimiento'
        ordering=['-fch_std_mov']
        

    def __str__(self) -> str:
       return f" id: {self.id_rec} --- {self.fch_mov} - [{self.id_rec.id_legajo} - {self.id_rec.id_tipo_rec.dsc_tipo_rec}] - Estado: {self.id_std_mov.dsc_std_mov}"
    
  
def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        
        val=unique_slug_generator(instance)
        instance.slug=slugify(val)
        
pre_save.connect(slug_generator, sender=Movimiento)


class HistMovimiento(models.Model):
    h_id_mov=models.AutoField(primary_key=True)
    id_mov=models.PositiveBigIntegerField()
    fch_mov=models.DateField(blank=False, null=False)
    id_rec=models.ForeignKey(Reclamo, on_delete=models.RESTRICT)
    id_std_mov=models.CharField(max_length=50)
    gde_mov=models.CharField(max_length=50, null=True,blank=True)
    obs_mov=models.CharField(max_length=200, null=True,blank=True)
    fch_std_mov=models.DateField(blank=False, null=False)
    fch_mov_user=models.DateTimeField(auto_now_add=True)
    user_mov=models.CharField(max_length=20)
    slug=models.CharField(max_length=200, null=True,blank=True)
    h_user_proc=models.ForeignKey(User, on_delete=models.RESTRICT)
    h_fch_proc=models.DateTimeField(auto_now_add=True)
    h_tipo_proc = models.CharField(max_length=1, null=True)
    
   
    
    
    class Meta:
        verbose_name='H_Movimiento'
        verbose_name_plural='H_Movimiento'
        ordering=['-h_fch_proc']
        

    def __str__(self) -> str:
       return f" {self.fch_mov_user} - [{self.id_std_mov} - {self.gde_mov} - {self.obs_mov}  - {self.h_fch_proc} : {self.h_user_proc} : {self.h_tipo_proc}"