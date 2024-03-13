from django import forms
from .models import Bien
from apps.clase.models import Clase
from apps.tipo.models import Tipo
from apps.marca.models import Marca
from apps.modelo.models import Modelo

cupi=forms.IntegerField(min_value=1)
clase=forms.ModelChoiceField(queryset=Clase.objects.all())
tipo=forms.ModelChoiceField(queryset=Tipo.objects.all())
marca=forms.ModelChoiceField(queryset=Marca.objects.all())
modelo=forms.ModelChoiceField(queryset=Modelo.objects.all())
gde_bien=forms.CharField()


class BienForm(forms.ModelForm):
    
    
    class Meta:
        model=Bien
        fields=['clase','tipo','marca','modelo','cupi','serie','nro_inventario','no_inventariado','obs_bien','gde_bien','qr_bien']
        labels={
                
                'clase': 'Clase',
                'tipo':'Tipo',
                'marca':'Marca',
                'modelo':'Modelo',
                'cupi':'Nro. Cupi',
                'serie':'Nro. Serie',
                'nro_inventario':'Nro. Inventario',
                'no_inventariado': 'Sin Inventario',
                'obs_bien':'Observacion',
                'gde_bien':'Nro. GDE',
                'qr_bien':'QR',
                
                
                }
       
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["gde_bien"].widget.attrs.update({"class": "form-control"})
            self.fields["clase"].widget.attrs.update(
            {
                'data-dropdown-parent':'#bien_card',
                'class':"form-control",
                'name':"clase",
                'id':"clase",
                'title':"clase",
                'style':"width: 100%", 
                'autofocus':True,
            }
        )
            
            self.fields["tipo"].widget.attrs.update(
            {
                'data-dropdown-parent':'#bien_card',
                'class':"form-control" ,
                'name':"tipo" ,
                'id':"tipo" ,
                'title':"tipo" ,
                'style':"width: 100%", 
            }
        )
            self.fields["marca"].widget.attrs.update(
                {
                    'data-dropdown-parent':'#bien_card',
                    'class':"form-control" ,
                    'name':"marca" ,
                    'id':"marca" ,
                    'title':"marca" ,
                    'style':"width: 100%", 
                }
            )
            self.fields["modelo"].widget.attrs.update(
                {
                    'data-dropdown-parent':'#bien_card',
                    'class':"form-control",
                    'name':"modelo",
                    'id':"modelo",
                    'title':"modelo",
                    'style':"width: 100%", 
                }            )
            
            
                
            

    def clean(self): 
       
        try:
            
            if not  self.cleaned_data.get('clase'):
                raise forms.ValidationError('Ingrese Clase')
            
            if not self.cleaned_data.get('tipo'):
                raise forms.ValidationError('Ingrese Tipo')
            
            if not self.cleaned_data.get('marca'):
                raise forms.ValidationError('Ingrese Marca')
            
            if not self.cleaned_data.get('modelo'):
                raise forms.ValidationError('Ingrese Modelo')
                        
            
            if not self.cleaned_data.get('cupi'):
                raise forms.ValidationError('Ingrese Nro. de Cupi')
                
            else:
                num_cupi=self.cleaned_data['cupi']
                buscar=Bien.objects.get(cupi=num_cupi)
            

            if not self.instance.pk:
                
                raise forms.ValidationError('El Nro. de CUPI esta Registrado') 
            elif self.instance.pk !=buscar.pk:
                
                raise forms.ValidationError('Cambio no Permitido, CUPI Existente')
            
            
            
            
        except Bien.DoesNotExist:
            
            pass
       
        return self.cleaned_data    
       
        
class InventariarForm(forms.ModelForm):
    class Meta:
        model=Bien
        fields=['cupi','serie','nro_inventario','obs_bien','gde_bien','no_inventariado']
        labels={
                'cupi':'Nro. Cupi',
                'serie':'Nro. Serie',
                'nro_inventario':'Nro. Inventario',
                'obs_bien':'Observacion',
                'gde_bien':'Nro. GDE',
                'no_inventariado': 'Sin Inventario',
                
                }
 

