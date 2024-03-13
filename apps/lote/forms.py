from django import forms
from .models import Lote
from datetime import date
from apps.rec_lote.models import Rec_Lote
from django.db.models import Sum,Count, Max, Min
import asyncio


class LoteForm(forms.ModelForm):
    class Meta:
        model=Lote
        fields=['year_lote','nivel_lote', 'importe_lote'] 
        
        
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['year_lote']=forms.IntegerField(min_value=date.today().year)
            self.fields['nivel_lote']=forms.IntegerField(min_value=1)
            self.fields['importe_lote']=forms.FloatField(min_value=0)
            
            self.fields["nivel_lote"].widget.attrs.update(
            {
                'class':"form-control",
                'name':"nivel_lote",
                'id':"nivel_lote",
                'title':"nivel_lote",
                'style':"width: 100%", 
                'autofocus':True,
            }
        ),
            self.fields["year_lote"].widget.attrs.update(
            {
                'class':"form-control",
                'name':"year_lote",
                'id':"year_lote",
                'title':"year_lote",
                'style':"width: 100%", 
                'autofocus':True,
            }
        ),
        
            self.fields["importe_lote"].widget.attrs.update(
            {
                'class':"form-control",
                'name':"importe_lote",
                'id':"importe_lote",
                'title':"importe_lote",
                'style':"width: 100%", 
                'autofocus':True,
            }
        )
            
           
    
    
    def clean(self): 
        
        try:
            nivel=self.cleaned_data.get("nivel_lote")
            year=self.cleaned_data.get("year_lote")
            total=self.cleaned_data.get("importe_lote")
           
            if not year:
                raise forms.ValidationError('Ingrese Año del Lote')
            
            
            buscar=Lote.objects.get(nivel_lote=nivel, year_lote=year) 
           
            
            if not self.instance.pk:
                
                raise forms.ValidationError('El Lote Existe') 
            elif self.instance.pk !=buscar.pk:
                
                raise forms.ValidationError('Cambio no Permitido, Lote Existente')
            
            print('hasta aca')
           
            loteinrec = Rec_Lote.objects.filter(id_lote=buscar.pk).aggregate(suma=Sum('id_rec__deudas_reclamos__total'))
            if total < loteinrec['suma']:
                raise forms.ValidationError('El Total del Lote es insuficiente')
            
            
            
            
           
            
            #print(loteinrec['suma'])
        except Lote.DoesNotExist:
           
                pass
        
        
       
        return self.cleaned_data
    