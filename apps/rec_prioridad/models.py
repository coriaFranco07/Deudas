from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify  #genera un slug a partir de una cadena de texto
from regunicopago.util import unique_slug_generator
from apps.reclamo.models import Reclamo
from apps.prioridad.models import Prioridad
from apps.movimiento.models import Movimiento
# Create your models here.

class Rec_Prioridad(models.Model):
    id_rec_prior=models.AutoField(primary_key=True)
    id_rec=models.OneToOneField(Reclamo, on_delete=models.RESTRICT, related_name='prioridad_reclamos')
    id_prior=models.ForeignKey(Prioridad, on_delete=models.RESTRICT)
    id_mov=models.ForeignKey(Movimiento, on_delete=models.RESTRICT, related_name='prioridad_movs')
    orden=models.PositiveIntegerField(default=0)
    fch_orden=models.DateField(auto_now=True, null=True, blank=True)
    norma_legal_prior=models.CharField(max_length=20, null=True)
    
    fch_rec_prior=models.DateTimeField(auto_now=True)
    user_rec_prior=models.ForeignKey(User, on_delete=models.RESTRICT)
    slug=models.SlugField(max_length=200, null=True,blank=True)
    
    
    
    
    class Meta:
        verbose_name='Prioridad de Reclamo'
        verbose_name_plural='Prioridad de Reclamos'
        ordering=['orden']
        

    def __str__(self) -> str:
       return f" [{self.orden}] - {self.id_rec} - [{self.id_prior.dsc_prior} - {self.id_rec.id_tipo_rec.dsc_tipo_rec}] - [{self.id_mov.id_std_mov.dsc_std_mov} - {self.id_mov.fch_mov}] ]"
    
  
def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        
        val=unique_slug_generator(instance)
        instance.slug=slugify(val)
        
pre_save.connect(slug_generator, sender=Rec_Prioridad)


class HistRec_Prioridad(models.Model):
    h_id_rec_prior=models.AutoField(primary_key=True)
    id_rec_prior=models.PositiveIntegerField()
    id_rec=models.OneToOneField(Reclamo, on_delete=models.RESTRICT)
    id_prior=models.ForeignKey(Prioridad, on_delete=models.RESTRICT)
    id_mov=models.ForeignKey(Movimiento, on_delete=models.RESTRICT)
    orden=models.PositiveIntegerField(default=0)
    fch_orden=models.DateField(auto_now=True, null=True, blank=True)
    norma_legal_prior=models.CharField(max_length=20, null=True)
    
    fch_rec_prior=models.DateTimeField(auto_now=True)
    user_rec_prior=models.CharField(max_length=20)
    slug=models.CharField(max_length=200, null=True,blank=True)
    
    h_user_proc=models.ForeignKey(User, on_delete=models.RESTRICT)
    h_fch_proc=models.DateTimeField(auto_now_add=True)
    h_tipo_proc = models.CharField(max_length=1, null=True)
    
    
    
    class Meta:
        verbose_name='H_Prioridad de Reclamo'
        verbose_name_plural='H_Prioridad de Reclamos'
        ordering=['-h_fch_proc']
        

    def __str__(self) -> str:
       return f"{self.id_rec} - {self.id_prior} - {self.id_mov} - {self.orden}: {self.h_fch_proc} : {self.h_user_proc} : {self.h_tipo_proc} "
    