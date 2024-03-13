from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils.text import slugify  #genera un slug a partir de una cadena de texto
from regunicopago.util import unique_slug_generator
from apps.estado.models import Estado
from django.contrib.contenttypes.fields import GenericRelation


class ControlEstado(models.Model):
    id_contro_std=models.AutoField(primary_key=True)
    
    
    std_origen=models.ForeignKey(Estado ,to_field='id_std' ,on_delete=models.CASCADE, related_name='std_orig', default=None)
    std_destino=models.ForeignKey(Estado ,to_field='id_std',on_delete=models.CASCADE, related_name='std_destino', default=None)
    
    fch_control_std=models.DateTimeField(auto_now=True)
    user_control_std=models.ForeignKey(User, on_delete=models.RESTRICT)
    slug=models.SlugField(max_length=200, null=True,blank=True)
   
    
    class Meta:
        verbose_name='Control Estado'
        verbose_name_plural='Controles Estados'
        ordering=['std_origen']
        

    def __str__(self) -> str:
       return f"{self.std_origen.dsc_std} A {self.std_destino.dsc_std} "
    
  
def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        
        val=unique_slug_generator(instance)
        instance.slug=slugify(val)
        
pre_save.connect(slug_generator, sender=ControlEstado)



class HistControlEstado(models.Model):
    h_id_contro_std=models.AutoField(primary_key=True)
    
    id_contro_std=models.PositiveIntegerField(null=True)
    std_origen=models.CharField(max_length=20, null=True)
    std_destino=models.CharField(max_length=20, null=True)
    fch_control_std=models.DateTimeField(null=True)
    user_control_std=models.CharField(max_length=20,null=True)
    slug_std=models.CharField(max_length=200, null=True,blank=True)
    h_user_proc=models.ForeignKey(User, on_delete=models.RESTRICT)
    h_fch_proc=models.DateTimeField(auto_now_add=True)
    h_tipo_proc = models.CharField(max_length=1, null=True)
    
    
    class Meta:
        verbose_name='H_Control Estado'
        verbose_name_plural='H_Controles Estados'
        ordering=['-h_fch_proc']
        

    def __str__(self) -> str:
       return f"{self.std_origen} - {self.std_destino} : {self.h_fch_proc} : {self.h_user_proc} : {self.h_tipo_proc} "