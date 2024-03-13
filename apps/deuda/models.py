from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify  #genera un slug a partir de una cadena de texto
from regunicopago.util import unique_slug_generator
from apps.reclamo.models import Reclamo

# Create your models here.

class Deuda(models.Model):
    id_deuda=models.AutoField(primary_key=True)
    id_rec=models.OneToOneField(Reclamo, on_delete=models.RESTRICT, related_name='deudas_reclamos')
    neto=models.FloatField(default=0)
    aportes=models.FloatField(default=0)
    contribuciones=models.FloatField(default=0)
    cargas=models.FloatField(default=0)
    interes=models.FloatField(default=0)
    otros=models.FloatField(default=0)
    total=models.FloatField(default=0)
    fch_calculo=models.DateField(blank=False, null=False)
    fch_deuda=models.DateTimeField(auto_now=True)
    user_deuda=models.ForeignKey(User, on_delete=models.RESTRICT)
    slug=models.SlugField(max_length=200, null=True,blank=True)
    
    
    
    
    class Meta:
        verbose_name='Deuda'
        verbose_name_plural='Deudas'
        ordering=['id_rec']
        
    def __str__(self) -> str:
       return f" {self.id_rec}  - [Neto: {self.neto} - Total: {self.total}] ]"
    
  
def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        
        val=unique_slug_generator(instance)
        instance.slug=slugify(val)
        
pre_save.connect(slug_generator, sender=Deuda)


class HistDeuda(models.Model):
    h_id_deuda=models.AutoField(primary_key=True)
    id_deuda=models.PositiveBigIntegerField()
    id_rec=models.OneToOneField(Reclamo, on_delete=models.RESTRICT)
    neto=models.FloatField(default=0)
    aportes=models.FloatField(default=0)
    contribuciones=models.FloatField(default=0)
    cargas=models.FloatField(default=0)
    interes=models.FloatField(default=0)
    otros=models.FloatField(default=0)
    total=models.FloatField(default=0)
    fch_calculo=models.DateField(blank=False, null=False)
    fch_deuda=models.DateTimeField(auto_now=True)
    user_deuda=models.CharField(max_length=20)
    slug=models.CharField(max_length=200, null=True,blank=True)
    
    h_user_proc=models.ForeignKey(User, on_delete=models.RESTRICT)
    h_fch_proc=models.DateTimeField(auto_now_add=True)
    h_tipo_proc = models.CharField(max_length=1, null=True)
    
    
    
    
    class Meta:
        verbose_name='H_Deuda'
        verbose_name_plural='H_Deudas'
        ordering=['-h_fch_proc']
        
    def __str__(self) -> str:
         return f"{self.id_rec}  [N:{self.neto} A:{self.aportes} Co:{self.contribuciones} Ca:{self.cargas} I:{self.interes} O:{self.interes} T:{self.total}] -  {self.h_fch_proc} : {self.h_user_proc} : {self.h_tipo_proc} "