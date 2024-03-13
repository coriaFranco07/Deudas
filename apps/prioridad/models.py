from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils.text import slugify  #genera un slug a partir de una cadena de texto
from regunicopago.util import unique_slug_generator

# Create your models here.

class Prioridad(models.Model):
    id_prior=models.AutoField(primary_key=True)
    dsc_prior=models.CharField(max_length=50)
    nivel_prior = models.PositiveIntegerField(default=0)
    fch_prior=models.DateTimeField(auto_now=True)
    user_prior=models.ForeignKey(User, on_delete=models.RESTRICT)
    slug=models.SlugField(max_length=200, null=True,blank=True)
   
    
    class Meta:
        verbose_name='Prioridad'
        verbose_name_plural='Prioridades'
        ordering=['nivel_prior']
        unique_together = ('dsc_prior','nivel_prior')

    def __str__(self) -> str:
       return f" {self.dsc_prior}-  (Nivel: {self.nivel_prior}) "
    
  
def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        
        val=unique_slug_generator(instance)
        instance.slug=slugify(val)
        
pre_save.connect(slug_generator, sender=Prioridad)


class HistPrioridad(models.Model):
    h_id_prior=models.AutoField(primary_key=True)
    id_prior=models.IntegerField()
    dsc_prior=models.CharField(max_length=50)
    nivel_prior = models.PositiveIntegerField(default=0)
    fch_prior=models.DateTimeField(auto_now=True)
    user_prior=models.CharField(max_length=20)
    slug=models.CharField(max_length=200, null=True,blank=True)
    h_user_proc=models.ForeignKey(User, on_delete=models.RESTRICT)
    h_fch_proc=models.DateTimeField(auto_now_add=True)
    h_tipo_proc = models.CharField(max_length=1, null=True)
   
    
    class Meta:
        verbose_name='H_Prioridad'
        verbose_name_plural='H_Prioridades'
        ordering=['-h_fch_proc']
        

    def __str__(self) -> str:
       return f"{self.dsc_prior} - {self.nivel_prior}: {self.h_fch_proc} : {self.h_user_proc} : {self.h_tipo_proc} "