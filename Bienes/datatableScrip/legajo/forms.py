from django import forms
from .models import Legajo


class LegajoForm(forms.ModelForm):
    class Meta:
        model=Legajo
        #fields=['nro_doc','nombres','jerarquia','cuerpo'] 
        fields=['id_legajo','nombres','jerarquia','cuerpo'] 
        
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            #self.fields['nro_doc']=forms.IntegerField(min_value=1, max_value=100000000)
            self.fields["id_legajo"].widget.attrs.update(
            {
                'class':"form-control",
                'name':"id_legajo",
                'id':"id_legajo",
                'title':"Nro. Documento",
                'style':"width: 100%", 
                'autofocus':True,
            }
        ),
            self.fields["nombres"].widget.attrs.update(
            {
                'class':"form-control",
                'name':"nombres",
                'id':"nombres",
                'title':"Apellidos y Nombres",
                'style':"width: 100%", 
                'autofocus':True,
            }
        ),
            self.fields["jerarquia"].widget.attrs.update(
            {
                'class':"form-control",
                'name':"jerarquia",
                'id':"jerarquia",
                'title':"Jerarquia o Clase",
                'style':"width: 100%", 
                'autofocus':True,
            }
        ),
            self.fields["cuerpo"].widget.attrs.update(
            {
                'class':"form-control",
                'name':"cuerpo",
                'id':"cuerpo",
                'title':"Cuerpo o Nivel",
                'style':"width: 100%", 
                'autofocus':True,
            }
        ),
            
           
    
    
    def clean(self): 
        
        try:
            #legajo=self.cleaned_data.get("nro_doc")
            legajo=self.cleaned_data.get("id_legajo")
            nom=self.cleaned_data.get("nombres")
            jerar=self.cleaned_data.get("jerarquia")
            cpo=self.cleaned_data.get("cuerpo")
            
            
           
            if not legajo:
                raise forms.ValidationError('Ingrese nro. doc.  de la persona')
            
            
            if not nom:
                raise forms.ValidationError('Ingrese nombre de la persona')
                                            
                                            
            if not jerar:
                raise forms.ValidationError('Ingrese jerarquia o clase de la persona')
                
            
            if not cpo:
                raise forms.ValidationError('Ingrese cuerpo de la persona')
            
            buscar=Legajo.objects.get(id_legajo=legajo) 
           
            
            if not self.instance.pk:
                
                raise forms.ValidationError('la Persona ya se encuentra cargada') 
            
            
            elif self.instance.pk !=buscar.pk:
                
                raise forms.ValidationError('Cambio no Permitido,  Persona Existente')
            
        except Legajo.DoesNotExist:
                     
            pass
        
        
       
        return self.cleaned_data
    
    def clean_nombres(self):
        return self.cleaned_data['nombres'].title()
    
    def clean_jerarquia(self):
        return self.cleaned_data['jerarquia'].title()
    
    def clean_cuerpo(self):
        return self.cleaned_data['cuerpo'].upper()