from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils.text import slugify  #genera un slug a partir de una cadena de texto
from regunicopago.util import unique_slug_generator

# Create your models here.

class Estado(models.Model):
    id_std=models.AutoField(primary_key=True)
    dsc_std=models.CharField(max_length=50, unique=True)
    act_calculo = models.BooleanField(default=True)
    permitido = models.BooleanField(default=True)
    fch_std=models.DateTimeField(auto_now=True)
    user_std=models.ForeignKey(User, on_delete=models.RESTRICT)
    slug=models.SlugField(max_length=200, null=True,blank=True)
   
    
    class Meta:
        verbose_name='Estado'
        verbose_name_plural='Estados'
        ordering=['dsc_std']
        

    def __str__(self) -> str:
       return f"{self.dsc_std} "
    
  
def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        
        val=unique_slug_generator(instance)
        instance.slug=slugify(val)
        
pre_save.connect(slug_generator, sender=Estado)



class HistEstado(models.Model):
    h_id_std=models.AutoField(primary_key=True)
    id_std=models.PositiveBigIntegerField() 
    dsc_std=models.CharField(max_length=50)
    act_calculo = models.BooleanField(default=True)
    permitido = models.BooleanField(default=True)
    fch_std=models.DateTimeField(auto_now=True)
    user_std=models.CharField(max_length=20)
    slug_std=models.CharField(max_length=200, null=True,blank=True)
    h_user_proc=models.ForeignKey(User, on_delete=models.RESTRICT)
    h_fch_proc=models.DateTimeField(auto_now_add=True)
    h_tipo_proc = models.CharField(max_length=1, null=True)
   
    
    class Meta:
        verbose_name='H_Estado'
        verbose_name_plural='H_Estados'
        ordering=['-h_fch_proc']
        

    def __str__(self) -> str:
       return f"{self.dsc_std}: {self.h_fch_proc} : {self.h_user_proc} : {self.h_tipo_proc} "