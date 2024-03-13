from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils.text import slugify  #genera un slug a partir de una cadena de texto
from inventario.util import unique_slug_generator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Create your models here.

class Oficina(models.Model):
    id_oficina=models.PositiveIntegerField(primary_key=True)
    dsc_oficina=models.CharField(max_length=50, unique=True)
    id_oficina_padre=models.ForeignKey("self", on_delete=models.PROTECT, blank=True,null=True, related_name='hijo')
    fch_oficina=models.DateTimeField(auto_now=True)
    user_oficina=models.ForeignKey(User, on_delete=models.RESTRICT, default=None)
    slug=models.SlugField(max_length=200, null=True,blank=True)
    
    
    
    
    class Meta:
        verbose_name='Oficina'
        verbose_name_plural='Oficinas'
        ordering=['dsc_oficina']

    def __str__(self) -> str:
        return f" {self.id_oficina} - {self.dsc_oficina} "
    
    """def clean(self) -> None: 
           
            ofi=Oficina.objects.filter(id_oficina=self.id_oficina)
            buscar=Oficina.objects.filter(dsc_oficina__iexact=self.dsc_oficina)
            padre=Oficina.objects.filter(id_oficina=self.id_oficina_padre_id).first()
            if self.slug:
                if self.id_oficina==self.id_oficina_padre_id:
                    raise ValueError('Oficina y Superior son iguales')
                buscar = buscar.exclude(pk=self.id_oficina)
                ofi=ofi.exclude(pk=self.id_oficina)  
            if buscar.exists():     
                raise ValueError('El Nombre de Oficina Existe')
            if ofi.exists():     
                raise ValueError('El Código de Oficina Existe')
            if not padre:
                raise ValueError('No existe Oficina Superior Ingresada') 
            if not self.id_oficina_padre_id==1:
                try:
                    result=[]
                    valor=oficinas_user(self.id_oficina_padre_id, result)
                    return super().clean()
                except:
                    raise ValueError('Verifique Oficina Padre, genera Bucle infinito')"""
   
            
def slug_generator(sender, instance, *args, **kwargs):
        if not instance.slug:
            
            val=unique_slug_generator(instance)
            instance.slug=slugify(val)
            
pre_save.connect(slug_generator, sender=Oficina)


"""def oficinas_user(id_oficina,result):
    
    result.append(id_oficina)
    oficina = Oficina.objects.filter(id_oficina_padre=id_oficina)
    if oficina:
        for of in oficina:
            result = oficinas_user(of.id_oficina, result)
    return result"""
