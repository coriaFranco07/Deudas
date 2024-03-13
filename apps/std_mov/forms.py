from django import forms
from .models import EstadoMov


class EstadoMovForm(forms.ModelForm):
    class Meta:
        model=EstadoMov
        fields=['dsc_std_mov'] 
        
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            self.fields["dsc_std_mov"].widget.attrs.update(
            {
                'class':"form-control",
                'name':"dsc_std_mov",
                'id':"dsc_std_mov",
                'title':"dsc_std_mov",
                'style':"width: 100%", 
                'autofocus':True,
            }
        ),
            
           
    
    
    def clean(self): 
        
        try:
            estadomov=self.cleaned_data.get("dsc_std_mov")
            
           
            if not estadomov:
                raise forms.ValidationError('Ingrese nombre del nuevo Estado')
            
            
            buscar=EstadoMov.objects.get(dsc_std_mov__iexact=estadomov) 
           
            
            if not self.instance.pk:
                
                raise forms.ValidationError('El Estado ya existe') 
            elif self.instance.pk !=buscar.pk:
                
                raise forms.ValidationError('Cambio no Permitido, Estado Existente')
            
        except EstadoMov.DoesNotExist:
           
            pass
        
        
       
        return self.cleaned_data
    
    def clean_dsc_std_mov(self):
        return self.cleaned_data['dsc_std_mov'].upper()