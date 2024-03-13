from django import forms
from .models import Prioridad


class PrioridadForm(forms.ModelForm):
    class Meta:
        model=Prioridad
        fields=['dsc_prior','nivel_prior'] 
        
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            self.fields["dsc_prior"].widget.attrs.update(
            {
                'class':"form-control",
                'name':"dsc_prior",
                'id':"dsc_prior",
                'title':"dsc_prior",
                'style':"width: 100%", 
                'autofocus':True,
            }
        ),
            self.fields["nivel_prior"].widget.attrs.update(
            {
                'class':"form-control",
                'name':"nivel_prior",
                'id':"nivel_prior",
                'title':"nivel_prior",
                'style':"width: 100%", 
                'autofocus':True,
            }
        )
            
           
    
    
    def clean(self): 
        
        try:
            prioridad=self.cleaned_data.get("dsc_prior")
            nivel=self.cleaned_data.get("nivel_prior")
           
            if not prioridad:
                raise forms.ValidationError('Ingrese nombre de la prioridad')
            
            
            buscar=Prioridad.objects.get(dsc_prior__iexact=prioridad) 
           
            
            if not self.instance.pk:
                
                raise forms.ValidationError('La Prioridad ya existe') 
            elif self.instance.pk !=buscar.pk:
                
                raise forms.ValidationError('Cambio no Permitido, Prioridad Existente')
            
            if nivel_existe(self, nivel):
                raise forms.ValidationError('Cambio no Permitido, Nivel Existente')
            
        except Prioridad.DoesNotExist:
           
            try:
            
            
           
                if not nivel:
                    raise forms.ValidationError('Ingrese Nivel de la prioridad')
            
            
                nivelbuscar= Prioridad.objects.get(nivel_prior=nivel)
                
          
            
                if not self.instance.pk:
                
                    raise forms.ValidationError('El nivel ya existe') 
                
                
                elif self.instance.pk !=nivelbuscar.pk:
                
                    raise forms.ValidationError('Cambio no Permitido, Nivel Existente')
           
            
            except Prioridad.DoesNotExist:
           
                pass
        
        
       
        return self.cleaned_data
    
    def clean_dsc_prior(self):
        return self.cleaned_data['dsc_prior'].upper()
    
    
def nivel_existe(self, nivel):
        result=False
        try:
            nivelbuscar= Prioridad.objects.get(nivel_prior=nivel)
            if self.instance.pk != nivelbuscar.pk:
                result=True
        
        except:
            pass
        
        finally:
            return result
        
       