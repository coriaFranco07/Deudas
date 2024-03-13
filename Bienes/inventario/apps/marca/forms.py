from django import forms
from .models import Marca


class MarcaForm(forms.ModelForm):
    class Meta:
        model=Marca
        fields=['dsc_marca']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["dsc_marca"].widget.attrs.update({"class": "form-control", 'autofocus':True})
    
    def clean(self): 
        
        try:
            marca=self.cleaned_data.get("dsc_marca")
           
            if not marca:
                raise forms.ValidationError('Ingrese la Descripción ')
            
            buscar=Marca.objects.get(dsc_marca__iexact=marca)
            

            if not self.instance.pk:
                
                raise forms.ValidationError('La Marca Existe.') 
            elif self.instance.pk !=buscar.pk:
                
                raise forms.ValidationError('Cambio no Permitido, Marca Existente')
            
            
        except Marca.DoesNotExist:
           
            pass
        
        
        print('++++++++++++++++++++++++++++++')
        return self.cleaned_data
    