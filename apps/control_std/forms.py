from django import forms
from .models import ControlEstado


class ControlEstadoForm(forms.ModelForm):
    class Meta:
        model= ControlEstado
        fields=['std_origen','std_destino'] 
        
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            self.fields["std_origen"].widget.attrs.update(
            {
                'class':"form-control",
                'name':"std_origen",
                'id':"std_origen",
                'title':"Origen",
                'style':"width: 100%", 
                'autofocus':True,
            }
        ),
            self.fields["std_destino"].widget.attrs.update(
            {
                'class':"form-control",
                'name':"std_destino",
                'id':"std_destino",
                'title':"Destino",
                'style':"width: 100%", 
                'autofocus':True,
                
            }
        ),
            
           
    
    
    def clean(self): 
        
        try:
            origen=self.cleaned_data.get("std_origen")
            destino=self.cleaned_data.get("std_destino")
            
           
            if not origen or not destino:
                raise forms.ValidationError('Ingrese combinacion de Estados')
            
            
            if origen == destino:
                raise forms.ValidationError('Ingrese combinaciones distintas')


            
                        
            buscar=ControlEstado.objects.get(std_origen=origen, std_destino=destino) 
           
            
            if not self.instance.pk:
                
                raise forms.ValidationError('La Combinacion Existe') 
            elif self.instance.pk !=buscar.pk:
                
                raise forms.ValidationError('Cambio no Permitido, Combinacion  Existente')
            
        except ControlEstado.DoesNotExist:
                     
            pass
        
        
       
        return self.cleaned_data
    