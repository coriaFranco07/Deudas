from django import forms
from .models import Rec_Prioridad
from apps.prioridad.models import Prioridad
from apps.movimiento.models import Movimiento

id_prior=forms.ModelChoiceField(queryset=Prioridad.objects.all())

class DateInput(forms.DateInput):
    input_type = 'date'

class RecPrioridadForm(forms.ModelForm):
    class Meta:
        model=Rec_Prioridad
        fields=['id_prior','norma_legal_prior']
       
        
    def __init__(self, *args, **kwargs):
            #slug_mov= kwargs.pop('slug_mov', None)
            #slug_rec_prior=kwargs.pop('slug_rec_prior', None)
            
            
            super().__init__(*args, **kwargs)
           
            
            
            self.fields["id_prior"].widget.attrs.update(
            {
                'data-dropdown-parent':'#oper_card',
                'class':"form-control",
                'name':"id_prior",
                'id':"id_prior",
                'title':"Establecer Prioridad",
                'style':"width: 100%", 
                'autofocus':True,
            }
        ),
            self.fields["norma_legal_prior"].widget.attrs.update(
            {
                
                'class':"form-control",
                'name':"norma_legal_prior",
                'id':"norma_legal_prior",
                'title':"Indicar Norma Legal",
                'style':"width: 100%", 
                'autofocus':True,
            }
         ),
        #     self.fields["orden"].widget.attrs.update(
        #     {
        #         'class':"form-control",
        #         'name':"orden",
        #         'id':"orden",
        #         'title':"Establecer Orden",
        #         'style':"width: 100%", 
        #         'autofocus':True,
        #     }
        # ),
           
       
           
    
    
    def clean(self): 
        
         try:
             
             pass
    #         prioridad=self.cleaned_data.get("dsc_prior")
    #         nivel=self.cleaned_data.get("nivel_prior")
           
    #         if not prioridad:
    #             raise forms.ValidationError('Ingrese nombre de la prioridad')
            
            
    #         buscar=Prioridad.objects.get(dsc_prior__iexact=prioridad) 
           
            
    #         if not self.instance.pk:
                
    #             raise forms.ValidationError('La Prioridad ya existe') 
    #         elif self.instance.pk !=buscar.pk:
                
    #             raise forms.ValidationError('Cambio no Permitido, Prioridad Existente')
            
         except Prioridad.DoesNotExist:
              pass
           
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
        
        
       
         return self.cleaned_data
    
    
    def clean_norma_legal_prior(self):
        return self.cleaned_data['norma_legal_prior'].upper()
    # def clean_dsc_prior(self):
    #     return self.cleaned_data['dsc_prior'].upper()