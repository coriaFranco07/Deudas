from django import forms
from .models import Estado


class EstadoForm(forms.ModelForm):
    dsc_estado=forms.CharField(min_length=3, max_length=30)
    class Meta:
        model=Estado
        fields=['dsc_estado','origen']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["dsc_estado"].widget.attrs.update({"class": "form-control", 'autofocus':True})
        self.fields["origen"].widget.attrs.update({"class": "form-check-input"})
        
    def clean(self): 
        
        try:
            estado=self.cleaned_data.get("dsc_estado")
           
            if not estado:
                raise forms.ValidationError('Ingrese la Descripción ')
            
            buscar=Estado.objects.get(dsc_estado__iexact=estado)
            

            if not self.instance.pk:
                
                raise forms.ValidationError('El Estado Existe.') 
            elif self.instance.pk !=buscar.pk:
                
                raise forms.ValidationError('Cambio no Permitido, Estado Existente')
            
            
        except Estado.DoesNotExist:
           
            pass
       
        return self.cleaned_data
    