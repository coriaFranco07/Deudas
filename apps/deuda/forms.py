from django import forms
from .models import Deuda
from datetime import date

class DateInput(forms.DateInput):
    input_type = 'date'

class DeudaForm(forms.ModelForm):
    class Meta:
        model=Deuda
        fields=['neto','aportes','contribuciones','cargas','interes','otros','total','fch_calculo'] 
        
        
        widgets = {
                'fch_calculo': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control', 
                'placeholder': 'Select a date',
                'type': 'date'
                }),
                
             }
        
        
        
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
                    
            self.fields['neto']=forms.FloatField(min_value=0)
            self.fields['aportes']=forms.FloatField(min_value=0)
            self.fields['contribuciones']=forms.FloatField(min_value=0)
            self.fields['cargas']=forms.FloatField(min_value=0)
            self.fields['interes']=forms.FloatField(min_value=0)
            self.fields['otros']=forms.FloatField(min_value=0)
            self.fields['total']=forms.FloatField(min_value=0)
            
            self.fields["neto"].widget.attrs.update(
            {
                'class':"form-control",
                'name':"dsc_prior",
                'id':"dsc_prior",
                'title':"dsc_prior",
                'style':"width: 100%", 
                'autofocus':True,
            }
        ),
            self.fields["aportes"].widget.attrs.update(
            {
                'class':"form-control",
                'name':"nivel_prior",
                'id':"nivel_prior",
                'title':"nivel_prior",
                'style':"width: 100%", 
                'autofocus':True,
            }
        ),
            self.fields["contribuciones"].widget.attrs.update(
            {
                'class':"form-control",
                'name':"nivel_prior",
                'id':"nivel_prior",
                'title':"nivel_prior",
                'style':"width: 100%", 
                'autofocus':True,
            }
        ),
            self.fields["cargas"].widget.attrs.update(
            {
                'class':"form-control",
                'name':"nivel_prior",
                'id':"nivel_prior",
                'title':"nivel_prior",
                'style':"width: 100%", 
                'autofocus':True,
            }
        ),
            self.fields["interes"].widget.attrs.update(
            {
                'class':"form-control",
                'name':"nivel_prior",
                'id':"nivel_prior",
                'title':"nivel_prior",
                'style':"width: 100%", 
                'autofocus':True,
            }
        ),
            self.fields["otros"].widget.attrs.update(
            {
                'class':"form-control",
                'name':"nivel_prior",
                'id':"nivel_prior",
                'title':"nivel_prior",
                'style':"width: 100%", 
                'autofocus':True,
            }
        ),
            self.fields["total"].widget.attrs.update(
            {
                'class':"form-control",
                'name':"nivel_prior",
                'id':"nivel_prior",
                'title':"nivel_prior",
                'style':"width: 100%", 
                'autofocus':True,
            }
        ),
            self.fields["fch_calculo"].widget.attrs.update(
            {
                'class':"form-control",
                'name':"fch_dsd_rec",
                'id':"fch_dsd_rec",
                'title':"fch_dsd_rec",
                'style':"width: 100%", 
                'autofocus':True,
                'input_type':'date'
                
            }
        )
            
           
    def clean_fch_calculo(self):
            fch_calculo = self.cleaned_data['fch_calculo']
            
            if fch_calculo > date.today():
                
                raise forms.ValidationError("Fecha de Calculo incorrecta")
            return fch_calculo
    
    # def clean(self): 
        
    #     try:
    #         prioridad=self.cleaned_data.get("dsc_prior")
    #         nivel=self.cleaned_data.get("nivel_prior")
           
    #         if not prioridad:
    #             raise forms.ValidationError('Ingrese nombre de la prioridad')
            
            
    #         buscar=Prioridad.objects.get(dsc_prior__iexact=prioridad) 
           
            
    #         if not self.instance.pk:
                
    #             raise forms.ValidationError('La Prioridad ya existe') 
    #         elif self.instance.pk !=buscar.pk:
                
    #             raise forms.ValidationError('Cambio no Permitido, Prioridad Existente')
            
    #     except Prioridad.DoesNotExist:
           
    #         try:
            
            
           
    #             if not nivel:
    #                 raise forms.ValidationError('Ingrese Nivel de la prioridad')
            
            
    #             nivelbuscar= Prioridad.objects.get(nivel_prior=nivel)
            
    #             if not self.instance.pk:
                
    #                 raise forms.ValidationError('El nivel ya existe') 
    #             elif self.instance.pk !=nivelbuscar.pk:
                
    #                 raise forms.ValidationError('Cambio no Permitido, Nivel Existente')
           
            
    #         except Prioridad.DoesNotExist:
           
    #             pass
        
        
       
    #     return self.cleaned_data
    
    # def clean_dsc_prior(self):
    #     return self.cleaned_data['dsc_prior'].upper()