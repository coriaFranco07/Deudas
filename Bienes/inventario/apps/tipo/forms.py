from django import forms
from .models import Tipo


class TipoForm(forms.ModelForm):
    dsc_tipo=forms.CharField(min_length=3, max_length=30)
    class Meta:
        model=Tipo
        fields=['dsc_tipo']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["dsc_tipo"].widget.attrs.update({"class": "form-control", 'autofocus':True})
        
    def clean(self): 
        
        try:
            tipo=self.cleaned_data.get("dsc_tipo")
           
            if not tipo:
                raise forms.ValidationError('Ingrese la Descripción ')
            
            buscar=Tipo.objects.get(dsc_tipo__iexact=tipo)
            

            if not self.instance.pk:
                
                raise forms.ValidationError('El Tipo Existe.') 
            elif self.instance.pk !=buscar.pk:
                
                raise forms.ValidationError('Cambio no Permitido, Tipo Existente')
            
            
        except Tipo.DoesNotExist:
           
            pass
       
        return self.cleaned_data
    