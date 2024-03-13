from typing import Any
from django import forms
from django.forms.fields import Field
from .models import MovData
from apps.oficina.models import Oficina
from apps.estado.models import Estado
from apps.bien.models import Bien


class MovDataForm(forms.ModelForm):
    class Meta:
        model=MovData
        fields=['bien_mov','estado','gde_mov','observ_mov','destino']
        labels={
                'bien_mov': 'Elemento',
                'estado': 'Estado',
                'gde_mov': 'Nro. GDE',
                'observ_mov': 'Observacion',
                'destino': 'Destino del Elemento',
                }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        self.fields["gde_mov"].widget.attrs.update({"class": "form-control", 'autofocus':True})
        self.fields["observ_mov"].widget.attrs.update({"class": "form-control"})
        self.fields["bien_mov"].widget.attrs.update(
            {
                'data-dropdown-parent':'#ofi_card',
                'class':"form-control" ,
                'name':"bien_mov" ,
                'id':"bien_mov" ,
                'title':"bien_mov" ,
                'style':"width: 100%", 
            }
        )
        self.fields["destino"].widget.attrs.update(
            {
                'data-dropdown-parent':'#ofi_card',
                'class':"form-control" ,
                'name':"destino" ,
                'id':"destino" ,
                'title':"destino" ,
                'style':"width: 100%", 
            }
        )
        self.fields["estado"].widget.attrs.update(
            {
                'data-dropdown-parent':'#ofi_card',
                'class':"form-control" ,
                'name':"estado" ,
                'id':"estado" ,
                'title':"estado" ,
                'style':"width: 100%", 
            }
        )
   
        
class RecuperarForm(forms.ModelForm):
    class Meta:
        model=MovData
        fields=['gde_mov','observ_mov']
        labels={
                'gde_mov': 'Nro. GDE',
                'observ_mov': 'Observacion',
                }
        widgets={
            
            'gde_mov':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'id':'gde_mov',
                    'name': 'gde_mov'
                }
            ),
            'observ_mov':forms.Textarea(
                attrs={
                    'class':'form-control',
                    'id':'observ_mov',
                    'name': 'observ_mov'
                }
            ),
            
        },
       
class TransferirForm(forms.ModelForm):
    estado=forms.ModelChoiceField(queryset=Estado.objects.all())
    data=forms.CharField()
    
    class Meta:
        model=MovData
        fields=['estado','gde_mov','observ_mov','destino']
        labels={
                'estado': 'Estado',
                'gde_mov': 'Nro. GDE',
                'observ_mov': 'Observacion',
                'destino': 'Destino del Elemento',
                }

    
    def __init__(self, request, result,slug, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data'].initial =slug
        self.fields['destino'].queryset=result
        #self.destino=forms.ModelChoiceField(queryset=result)
        self.estado=forms.ModelChoiceField(queryset=Estado.objects.all())
        self.fields["gde_mov"].widget.attrs.update({"class": "form-control", 'autofocus':True})
        self.fields["observ_mov"].widget.attrs.update({"class": "form-control"})
        self.fields["destino"].widget.attrs.update(
            {
                'data-dropdown-parent':'#ofi_card',
                'class':"form-control" ,
                'name':"destino" ,
                'id':"destino" ,
                'title':"destino" ,
                'style':"width: 100%", 
            }
        )
        self.fields["estado"].widget.attrs.update(
            {
                'data-dropdown-parent':'#ofi_card',
                'class':"form-control" ,
                'name':"estado" ,
                'id':"estado" ,
                'title':"estado" ,
                'style':"width: 100%", 
            }
        )


class AdquirirForm(forms.ModelForm):
    #data=forms.CharField()
    
    class Meta:
        
            model=MovData
            fields=['gde_mov','observ_mov']
            labels={
                    'gde_mov': 'Nro. GDE',
                    'observ_mov': 'Observacion',
                    }
            widgets={
                
                'gde_mov':forms.TextInput(
                    attrs={
                        'class':'form-control',
                        'id':'gde_mov',
                        'name': 'gde_mov'
                    }
                ),
                'observ_mov':forms.Textarea(
                    attrs={
                        'class':'form-control',
                        'id':'observ_mov',
                        'name': 'observ_mov'
                    }
                ),
                
            },
        
            
                
    
            