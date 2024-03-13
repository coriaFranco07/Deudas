from django import forms
from django.contrib.auth.models import User
from .models import Operador
from apps.oficina.models import Oficina

oficina=forms.ModelChoiceField(queryset=Oficina.objects.all())
operador=forms.ModelChoiceField(queryset=User.objects.all())
class OperadorForm(forms.ModelForm):
    class Meta:
        model=Operador
        fields=['operador','oficina']
        labels={
                'operador': 'Operador',
                'oficina':'Destino',
                
                }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["operador"].widget.attrs.update(
            {
               'data-dropdown-parent':'#oper_card',
                'class':"form-control" ,
                'name':"operador" ,
                'id':"operador" ,
                'title':"operador" ,
                'style':"width: 100%", 
            }
        )
        self.fields["oficina"].widget.attrs.update(
            {
               'data-dropdown-parent':'#oper_card',
                'class':"form-control" ,
                'name':"oficina" ,
                'id':"oficina" ,
                'title':"oficina" ,
                'style':"width: 100%", 
            }
        )
            
        if self.instance.slug:
            self.fields["operador"].widget.attrs.update(
            {
               'data-dropdown-parent':'#oper_card',
                'class':"form-control" ,
                'name':"operador" ,
                'id':"operador" ,
                'title':"operador" ,
                'style':"width: 100%", 
            }
        )
            self.fields["oficina"].widget.attrs.update(
            {
               'data-dropdown-parent':'#oper_card',
                'class':"form-control" ,
                'name':"oficina" ,
                'id':"oficina" ,
                'title':"oficina" ,
                'style':"width: 100%", 
            }
        )
            

            
        def clean(self): 
       
               
                    
                    if not  self.cleaned_data.get('operador'):
                        raise forms.ValidationError('Ingrese Operador')
                    
                    if not self.cleaned_data.get('oficina'):
                        raise forms.ValidationError('Ingrese Oficina')
                    
                    operador=self.cleaned_data.get('operador')
                    oficina=self.cleaned_data.get('oficina')
                    data=Operador.objects.filter(operador=operador).exists()
                    dataOf=Operador.objects.filter(operador=operador, oficina=oficina).exists()
                                       
                    if dataOf:
                        raise forms.ValidationError('El Registro Existe, verifique')
                    if data:
                        raise forms.ValidationError('El Operador esta en Otra Dependencia')
                    
                    
                
            
                    return self.cleaned_data    
                