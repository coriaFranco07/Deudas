from django import forms
from .models import Clase



class ClaseForm(forms.ModelForm):
    dsc_clase=forms.CharField(min_length=3, max_length=30)
    class Meta:
        model=Clase
        fields=['dsc_clase']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["dsc_clase"].widget.attrs.update({"class": "form-control", 'autofocus':True})
            

    def clean(self): 
        
        try:
            
            clase=self.cleaned_data.get("dsc_clase")
           
            if not clase:
                raise forms.ValidationError('Ingrese la Descripción ')
            
            buscar=Clase.objects.get(dsc_clase__iexact=clase)
            

            if not self.instance.pk:
                
                raise forms.ValidationError('La Clase Existe.') 
            elif self.instance.pk !=buscar.pk:
                
                raise forms.ValidationError('Cambio no Permitido, Clase Existente')
            
            
        except Clase.DoesNotExist:
           
            pass
       
        return self.cleaned_data
    