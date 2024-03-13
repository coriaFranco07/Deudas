from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify  #genera un slug a partir de una cadena de texto
from regunicopago.util import unique_slug_generator
from apps.tipo_reclamo.models import TipoReclamo
from apps.legajo.models import Legajo
from apps.estado.models import Estado
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
def get_std():
    data=Estado.objects.get(dsc_std__iexact="activo")    
    return data.id_std

class Reclamo(models.Model):
    id_rec=models.AutoField(primary_key=True)
    id_legajo=models.ForeignKey(Legajo, on_delete=models.RESTRICT,related_name='legajos')
    id_tipo_rec=models.ForeignKey(TipoReclamo, on_delete=models.RESTRICT,related_name='tipos_reclamos')
    fch_dsd_rec=models.DateField(blank=False, null=False)
    fch_hst_rec=models.DateField(blank=False, null=False)
    dias_rec=models.PositiveIntegerField(default=0)
    norma_legal_rec=models.CharField(max_length=20, null=True)
    
    resol_pago_rec=models.CharField(max_length=20, null=True, blank=True)
    nro_supl = models.PositiveBigIntegerField(validators=[MinValueValidator(1)], null=True, blank=True)
    year_credito = models.PositiveSmallIntegerField(validators=[MinValueValidator(2022), MaxValueValidator(2050)], null=True, blank=True)
    #activo_rec=models.BooleanField(default=True)
    std_rec=models.ForeignKey(Estado, on_delete=models.RESTRICT,related_name='estado_reclamos', default=get_std())
    gde_mov=models.CharField(max_length=50, null=True,blank=True)
    fch_rec=models.DateTimeField(auto_now=True)
    user_rec=models.ForeignKey(User, on_delete=models.RESTRICT)
    slug=models.SlugField(max_length=200, null=True,blank=True)
    
    
    
    
    class Meta:
        verbose_name='Reclamo'
        verbose_name_plural='Reclamos'
        ordering=['fch_dsd_rec']
        unique_together = ('id_legajo','fch_dsd_rec','fch_hst_rec', 'id_tipo_rec')

    def __str__(self) -> str:
       return f" NRO:  {self.id_rec} - [{self.id_legajo}] - [{self.fch_dsd_rec} - {self.fch_hst_rec}] - [{self.id_tipo_rec}] - [{self.std_rec.dsc_std}]"
    
  
def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        
        val=unique_slug_generator(instance)
        instance.slug=slugify(val)
        
pre_save.connect(slug_generator, sender=Reclamo)


class HistReclamo(models.Model):
    h_id_rec=models.AutoField(primary_key=True)
    id_rec=models.PositiveBigIntegerField()
    id_legajo=models.ForeignKey(Legajo, on_delete=models.RESTRICT)
    id_tipo_rec=models.ForeignKey(TipoReclamo, on_delete=models.RESTRICT)
    fch_dsd_rec=models.DateField(blank=False, null=False)
    fch_hst_rec=models.DateField(blank=False, null=False)
    dias_rec=models.PositiveIntegerField(default=0)
    norma_legal_rec=models.CharField(max_length=20, null=True, blank=True)
    resol_pago_rec=models.CharField(max_length=20, null=True, blank=True)
    nro_supl = models.PositiveBigIntegerField(null=True, blank=True)
    year_credito = models.PositiveSmallIntegerField( null=True, blank=True) 
    gde_mov=models.CharField(max_length=50, null=True,blank=True)
    std_rec=models.ForeignKey(Estado, on_delete=models.RESTRICT)
    fch_rec=models.DateTimeField(auto_now=True)
    user_rec=models.CharField(max_length=20)
    slug=models.CharField(max_length=200, null=True,blank=True)
    
    h_user_proc=models.ForeignKey(User, on_delete=models.RESTRICT)
    h_fch_proc=models.DateTimeField(auto_now_add=True)
    h_tipo_proc = models.CharField(max_length=1, null=True)
    
    
    
    
    class Meta:
        verbose_name='H_Reclamo'
        verbose_name_plural='H_Reclamos'
        ordering=['-h_fch_proc']

    def __str__(self) -> str:
        return f"{self.id_legajo} - {self.id_tipo_rec} - {self.fch_dsd_rec} - {self.fch_hst_rec} - {self.std_rec}: {self.h_fch_proc} : {self.h_user_proc} : {self.h_tipo_proc} "
    