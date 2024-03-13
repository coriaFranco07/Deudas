from django import forms
from .models import TipoReclamo


class TipoRecForm(forms.ModelForm):
    class Meta:
        model=TipoReclamo
        fields=['codigo_rec','dsc_tipo_rec','tipo_anual'] 
        
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["dsc_tipo_rec"].widget.attrs.update(
            {
                'class':"form-control",
                'name':"codigo_rec",
                'id':"codigo_rec",
                'title':"Codigo Rec.",
                'style':"width: 100%", 
                'autofocus':True,
            }
        ),
            self.fields["dsc_tipo_rec"].widget.attrs.update(
            {
                'class':"form-control",
                'name':"dsc_tipo_rec",
                'id':"dsc_tipo_rec",
                'title':"dsc_tipo_rec",
                'style':"width: 100%", 
                'autofocus':True,
            }
        ),
            self.fields["tipo_anual"].widget.attrs.update(
            {
                'class':"form-check-input",
                'name':"tipo_anual",
                'id':"tipo_anual",
                'title':"Solo Periodos Anuales",
                'style':"width: 30%", 
                'autofocus':True,
                'type':"checkbox",
            }
        )
            
    def clean(self): 
        
        try:
            tiporeclamo=self.cleaned_data.get("dsc_tipo_rec")
            codigoreclamo=self.cleaned_data.get("codigo_rec")
            
           
            if not tiporeclamo:
                raise forms.ValidationError('Ingrese Desc. Tipo de Reclamo')
            
            if not codigoreclamo:
                raise forms.ValidationError('Ingrese Codigo de Reclamo')
            
            
            buscar=TipoReclamo.objects.get(dsc_tipo_rec__iexact=tiporeclamo) 
           
            
            if not self.instance.pk:
                
                raise forms.ValidationError('El Tipo de Reclama Existe') 
            elif self.instance.pk !=buscar.pk:
                
                raise forms.ValidationError('Cambio no Permitido, Tipo Existente')
            
            if codigo_existe(self, codigoreclamo):
                
                raise forms.ValidationError('Cambio no Permitido, Codigo Existente')
                
            
        except TipoReclamo.DoesNotExist:
           
                try:
            
            
           
                            if not codigoreclamo:
                                raise forms.ValidationError('Ingrese Codigo Tipo de Estado')
                        
                        
                            codigobuscar= TipoReclamo.objects.get(codigo_rec=codigoreclamo)
                            
                    
                        
                            if not self.instance.pk:
                            
                                raise forms.ValidationError('El Codigo existe') 
                            
                            
                            elif self.instance.pk !=codigobuscar.pk:
                            
                                raise forms.ValidationError('Cambio no Permitido, Codigo Existente')
                    
            
                except TipoReclamo.DoesNotExist:
           
                        pass
        
        
       
        return self.cleaned_data
    
    
    def clean_dsc_tipo_rec(self):
            return self.cleaned_data['dsc_tipo_rec'].upper()
        
        
        
def codigo_existe(self, codigoreclamo):
        result=False
        try:
            codigobuscar= TipoReclamo.objects.get(codigo_rec=codigoreclamo)
            if self.instance.pk != codigobuscar.pk:
                result=True
        
        except:
            pass
        
        finally:
            return result
        
          