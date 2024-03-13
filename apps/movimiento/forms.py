from django import forms
from .models import Movimiento
from apps.std_mov.models import EstadoMov
from apps.reclamo.models import Reclamo
id_std_mov=forms.ModelChoiceField(queryset=EstadoMov.objects.all())
from datetime import date


class DateInput(forms.DateInput):
    input_type = 'date'

class MovimientoForm(forms.ModelForm):
    gde_mov = forms.CharField(min_length=10,max_length=50)
    obs_mov = forms.CharField(max_length=200, required=False)
    class Meta:
        model=Movimiento
        fields=['fch_mov', 'id_std_mov','fch_std_mov', 'gde_mov', 'obs_mov']
       
        widgets = {
            'fch_mov': forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={'class': 'form-control', 
               'placeholder': 'Select a date',
               'type': 'date'
            }),
            'fch_std_mov': forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={'class': 'form-control', 
               'placeholder': 'Select a date',
               'type': 'date'
            }),
            
        }
        
    def __init__(self, *args, **kwargs):
            slug= kwargs.pop('slug', None)
            dia=date.today()           
            super().__init__(*args, **kwargs)
            
            #self.fields['fch_mov']=forms.DateField(min=date.today())
            self.fields['gde_mov']=forms.CharField(min_length=20, max_length=70)
           
            
            self.fields["fch_mov"].widget.attrs.update(
            {
                'class':"form-control",
                'name':"fch_mov",
                'id':"fch_mov",
                'title':"Fecha del Expte",
                'style':"width: 100%", 
                'autofocus':True,
            }
        ),
            self.fields["id_std_mov"].widget.attrs.update(
            {
                'data-dropdown-parent':'#oper_card',
                'class':"form-control",
                'name':"id_std_mov",
                'id':"Tipo de Movimiento",
                'title':"id_std_mov",
                'style':"width: 100%", 
                'autofocus':True,
            }
        ),
            
           
            self.fields["fch_std_mov"].widget.attrs.update(
            {
                'class':"form-control",
                'name':"fch_std_mov",
                'id':"fch_std_mov",
                'title':"Fecha que tomo el Estado",
                'style':"width: 100%", 
                'autofocus':True,
            }
        ),
            self.fields["gde_mov"].widget.attrs.update(
            {
                'class':"form-control",
                'name':"gde_mov",
                'id':"gde_mov",
                'title':"Nro. GDE EX-CCOO-GDEO",
                'style':"width: 100%", 
                'autofocus':True,
            }
        ),    
            self.fields["obs_mov"].widget.attrs.update(
            {
                'class':"form-control",
                'name':"obs_mov",
                'id':"obs_mov",
                'title':"Observaciones",
                'style':"width: 100%", 
                'autofocus':True,
            }
        ),   
   
   
    def clean_fch_mov(self):
            fch_calculo = self.cleaned_data['fch_mov']
            
            if fch_calculo > date.today():
                
                raise forms.ValidationError("Fecha Expediente incorrecta")
            return fch_calculo    
        
    def clean_fch_std_mov(self):
            fch_calculo = self.cleaned_data['fch_std_mov']
            
            if fch_calculo > date.today():
                
                raise forms.ValidationError("Fecha Vigencia Estado incorrecta")
            return fch_calculo 
        
    