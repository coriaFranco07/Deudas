from django import forms
from .models import Modelo


class ModeloForm(forms.ModelForm):
    dsc_modelo=forms.CharField(min_length=3, max_length=30)
    class Meta:
        model=Modelo
        fields=['dsc_modelo']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["dsc_modelo"].widget.attrs.update({"class": "form-control", 'autofocus':True})
        
    def clean(self): 
       
        try:
            modelo=self.cleaned_data.get("dsc_modelo")
           
            if not modelo:
                raise forms.ValidationError('Ingrese la Descripción ')
            
            buscar=Modelo.objects.get(dsc_modelo__iexact=modelo)
            

            if not self.instance.pk:
                
                raise forms.ValidationError('El Modelo Existe.') 
            elif self.instance.pk !=buscar.pk:
                
                raise forms.ValidationError('Cambio no Permitido, Modelo Existente')
            
            
        except Modelo.DoesNotExist:
            
            pass
       
        return self.cleaned_data
    