from django import forms
from .models import Estado


class EstadoForm(forms.ModelForm):
    class Meta:
        model=Estado
        fields=['dsc_std','act_calculo','permitido'] 
        
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            self.fields["dsc_std"].widget.attrs.update(
            {
                'class':"form-control",
                'name':"dsc_std",
                'id':"dsc_std",
                'title':"dsc_std",
                'style':"width: 100%", 
                'autofocus':True,
            }
        ),
            self.fields["act_calculo"].widget.attrs.update(
            {
                'class':"form-check-input",
                'name':"act_calculo",
                'id':"act_calculo",
                'title':"act_calculo",
                'style':"width: 30%", 
                'autofocus':True,
                 'type':"checkbox",
            }
        ),
            self.fields["permitido"].widget.attrs.update(
            {
                'class':"form-check-input",
                'name':"permitido",
                'id':"permitido",
                'title':"permitido",
                'style':"width: 30%", 
                'autofocus':True,
                'type':"checkbox",
            }
        )
            
           
    
    
    def clean(self): 
        
        try:
            estado=self.cleaned_data.get("dsc_std")
            
           
            if not estado:
                raise forms.ValidationError('Ingrese nombre del Estadp')
            
            
            buscar=Estado.objects.get(dsc_std__iexact=estado) 
           
            
            if not self.instance.pk:
                
                raise forms.ValidationError('El Estado ya existe') 
            elif self.instance.pk !=buscar.pk:
                
                raise forms.ValidationError('Cambio no Permitido, Estado Existente')
            
        except Estado.DoesNotExist:
                     
            pass
        
        
       
        return self.cleaned_data
    
    def clean_dsc_std(self):
        return self.cleaned_data['dsc_std'].upper()