from django import forms
from .models import Reclamo
from datetime import date
from django.utils import timezone
from .widget import DatePickerInput, TimePickerInput, DateTimePickerInput
from apps.legajo.models import Legajo
from apps.tipo_reclamo.models import TipoReclamo
from apps.estado.models import Estado
from apps.control_std.models import ControlEstado


id_legajo=forms.ModelChoiceField(queryset=Legajo.objects.all())
id_tipo_rec=forms.ModelChoiceField(queryset=TipoReclamo.objects.all())

class DateInput(forms.DateInput):
    input_type = 'date'
    
class ReclamoForm(forms.ModelForm):
    class Meta:
        model=Reclamo
        fields=['id_legajo','id_tipo_rec','fch_dsd_rec','fch_hst_rec', 'dias_rec', 'norma_legal_rec','std_rec','gde_mov'] 
        
        widgets = {
            'fch_dsd_rec': forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={'class': 'form-control', 
               'placeholder': 'Select a date',
               'type': 'date'
            }),
            'fch_hst_rec': forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={'class': 'form-control', 
               'placeholder': 'Select a date',
               'type': 'date'
            }),
            
        }
        
       
        
    def __init__(self, *args, **kwargs):
        
            
            required= kwargs.pop('required', True)
            
        
            super().__init__(*args, **kwargs)
            
            self.fields['gde_mov']=forms.CharField(min_length=20, max_length=50, required=required)
            self.fields['dias_rec']=forms.IntegerField(min_value=0, initial=0)
            self.fields['norma_legal_rec']=forms.CharField(max_length=20)
            
            
            self.fields["id_legajo"].widget.attrs.update(
            {
                'data-dropdown-parent':'#oper_card',
                'class':"form-control",
                'name':"id_legajo",
                'id':"id_legajo",
                'title':"Legajo",
                'style':"width: 100%", 
                'autofocus':True,
            }
        ),
            self.fields["id_tipo_rec"].widget.attrs.update(
            {
                'data-dropdown-parent':'#oper_card',
                'class':"form-control",
                'name':"id_tipo_rec",
                'id':"id_tipo_rec",
                'title':"Tipo de Reclamo",
                'style':"width: 100%", 
                'autofocus':True,
            }
        ),
            self.fields["fch_dsd_rec"].widget.attrs.update(
            {
                'class':"form-control",
                'name':"fch_dsd_rec",
                'id':"fch_dsd_rec",
                'title':"Fecha Desde",
                'style':"width: 100%", 
                'autofocus':True,
                'input_type':'date'
                
            }
        ),
            self.fields["norma_legal_rec"].widget.attrs.update(
            {
                'class':"form-control",
                'name':"norma_legal_rec",
                'id':"norma_legal_rec",
                'title':"Resolucion ",
                'style':"width: 100%", 
                'autofocus':True,
                
                
            }
        ),
            self.fields["fch_hst_rec"].widget.attrs.update(
            {
                'class':"form-control",
                'name':"fch_hst_rec",
                'id':"fch_hst_rec",
                'title':"Fecha Hasta",
                'style':"width: 100%", 
                'autofocus':True,
                'type':'date'
            }
        ),
            self.fields["dias_rec"].widget.attrs.update(
            {
                'class':"form-control",
                'name':"dias",
                'id':"dias",
                'title':"Dias",
                'style':"width: 100%", 
                'autofocus':True,
            }
        ),
            self.fields["gde_mov"].widget.attrs.update(
            {
                'class':"form-control",
                'name':"gde_mov",
                'id':"gde_mov",
                'title':"nro. gde.",
                'style':"width: 100%", 
                'autofocus':True,
            }
        ),
            self.fields["std_rec"].widget.attrs.update(
            {
                'data-dropdown-parent':'#oper_card',
                'class':"form-control",
                'name':"std_rec",
                'id':"std_rec",
                'title':"Estado del Reclamo",
                'style':"width: 100%", 
                'autofocus':True,
            }
        ),
            self.fields['std_rec'].queryset = Estado.objects.filter(permitido=True)
            
           
            
        
    
            
    def clean(self): 
        
        try:
            legajo=self.cleaned_data.get("id_legajo")
            
            desde=self.cleaned_data.get("fch_dsd_rec")
            
            hasta=self.cleaned_data.get("fch_hst_rec")
            
            tipo=self.cleaned_data.get("id_tipo_rec")
            
            std_rec=self.cleaned_data.get("std_rec")
            
            dias_in=self.cleaned_data.get('dias_rec')
            
            gde_mov=self.cleaned_data.get('gde_mov')
            
           
            
           
            if not legajo or not desde or not hasta or not tipo or not gde_mov:
                raise forms.ValidationError('Verifique datos del reclamo')
            
               
            
            if hasta < desde or hasta > date.today() or desde>date.today():
                raise forms.ValidationError('Verifique Fechas Desde - Hasta')
            
            
            
            
            #buscar=Reclamo.objects.get(id_legajo=legajo, fch_dsd_rec=desde, fch_hst_rec=hasta, id_tipo_rec=tipo) 
            buscar=Reclamo.objects.filter(id_legajo=legajo, id_tipo_rec=tipo)[:1].get()
            
            
            if self.instance.slug:
                pk=self.instance.slug
            else:
                pk=None   
               
                         
            if verificar_periodos(legajo, tipo,desde, hasta, pk):
                    raise forms.ValidationError('El reclamo comparte periodo con otro reclamo')
            
           
            if control_estdo(std_rec, pk):
                
                raise forms.ValidationError('El cambioi de Estado no esta permitido')
           
            # if not self.instance.pk:
                
            #     raise forms.ValidationError('El Reclamo Existe') 
            
            # elif self.instance.pk !=buscar.pk:
                
            #     raise forms.ValidationError('Cambio no Permitido, Reclamo Existente')
            
            
            
            
        
        except Reclamo.DoesNotExist:
            
                
        
                pass
            
        finally:
            
            
            if control_tipo_anual(tipo, desde, hasta) :
                
                    raise forms.ValidationError('El tipo de Reclamo, debe estar entre el 01/01 y el 31/12')
            
            dia=(hasta-desde).days + 1    
            if not tipo.tipo_anual:
                        dia=(hasta-desde).days + 1                        
                        if dias_in !=dia:
                    
                            raise forms.ValidationError(f'los dias de reclamo deberian ser {dia} ')
            else:
                        
                        if dias_in > (int(dia)):
                            raise forms.ValidationError('los dias superan el periodo requerido')
                    
                    
                            
                
    def clean_gde_mov(self):
        return self.cleaned_data['gde_mov'].upper()            
                    
        
    
    def clean_norma_legal_rec(self):
        return self.cleaned_data['norma_legal_rec'].upper()
    
    
    # def clean_dias_rec(self):
    #         desde=self.cleaned_data.get("fch_dsd_rec")
            
    #         hasta=self.cleaned_data.get("fch_hst_rec")
            
    #         tipo=self.cleaned_data.get("id_tipo_rec")
    #         dias_in=self.cleaned_data.get('dias_rec')
            
            
    #         dia=(hasta-desde).days + 1
            
    #         if not tipo.tipo_anual:
            
    #             if dias_in !=dia:
                    
    #                 raise forms.ValidationError(f'los dias de reclamo deberian ser {dia} ')
            
    #         return self.cleaned_data['dias_rec']
            



class SuplForm(forms.ModelForm):
    class Meta:
        model=Reclamo
        fields=['resol_pago_rec','nro_supl','year_credito'] 
        
             
       
        
    def __init__(self, *args, **kwargs):
        
            
            
        
            super().__init__(*args, **kwargs)
            
            self.fields['nro_supl']=forms.IntegerField(min_value=1, required=False)
            self.fields['year_credito']=forms.IntegerField(min_value=2022, max_value=2050, required=False)
            self.fields['resol_pago_rec']=forms.CharField(max_length=20, required=False)
            
            
            self.fields["nro_supl"].widget.attrs.update(
            {
                
                'class':"form-control",
                'name':"nro_supl",
                'id':"nro_supl",
                'title':"Suplementaria nro.",
                'style':"width: 100%", 
                'autofocus':True,
            }
        ),
            self.fields["resol_pago_rec"].widget.attrs.update(
            {
                
                'class':"form-control",
                'name':"resol_pago_rec",
                'id':"resol_pago_rec",
                'title':"Resolucion de Pago",
                'style':"width: 100%", 
                'autofocus':True,
            }
        ),
            self.fields["year_credito"].widget.attrs.update(
            {
                'class':"form-control",
                'name':"year_credito",
                'id':"year_credito",
                'title':"Año de Credito",
                'style':"width: 100%", 
                'autofocus':True,
                
                
            }
        ),
            
    def clean(self): 
        
        try:
            nro_supl=self.cleaned_data.get("nro_supl")
            
            year_credito=self.cleaned_data.get("year_credito")
            
            resol_pago_rec=self.cleaned_data.get("resol_pago_rec")
            
            
            
           
            
           
            if not resol_pago_rec:
                raise forms.ValidationError('Verifique Resolución de Pago')
            
           
            if (nro_supl and not year_credito or (not nro_supl and year_credito)):
                 raise forms.ValidationError('Verifique Nro. Sup. y Año de Credito')  
           
            
            
            if year_credito and year_credito > date.today().year:
                    
                    raise forms.ValidationError(f'El Año de Credito no puede ser suprior a {date.today().year}')
            
            
            
            if nro_supl: 
            
                buscar_nro_supl=Reclamo.objects.filter(nro_supl=nro_supl)[:1].get()
            
                                
                
                if buscar_nro_supl.year_credito != year_credito:
                    
                    raise forms.ValidationError(f'Suplementaria con Distinto Año, Verifique {buscar_nro_supl.year_credito}')
                    
                
             
            
        
        except Reclamo.DoesNotExist:
            
                
        
                pass
            
        
                            
                
    def clean_resol_pago_rec(self):
        return self.cleaned_data['resol_pago_rec'].upper()            
                    
            
       
       
    
 
                
def verificar_periodos(legajo, tipo, desde, hasta, pk=None):
        
            
            des=Reclamo.objects.filter(fch_dsd_rec__range=[desde,hasta]).filter(id_legajo=legajo).filter(id_tipo_rec=tipo).values() 
            if des.exists():
            
                for d in des:
                    
                    if d['slug'] != pk:
                        return True
                    
            
           
            has=Reclamo.objects.filter(fch_hst_rec__range=[desde,hasta]).filter(id_legajo=legajo).filter(id_tipo_rec=tipo).values()
            if has.exists():  
            
                for h in has:
                    
                    if h['slug'] != pk:
                        return True
           
            
            med=Reclamo.objects.filter(fch_dsd_rec__lte=desde).filter(fch_hst_rec__gte=desde).filter(id_legajo=legajo).filter(id_tipo_rec=tipo).values()
            if med.exists():  
                
                for m in med:
                    
                    if m['slug'] != pk:
                        return True
           
           
           
            
            return False
        
def control_estdo(std_reclamo, slug):
        
            estado=Reclamo.objects.get(slug=slug)
            control=ControlEstado.objects.filter(std_origen=estado.std_rec, std_destino=std_reclamo)
            #std = Estado.objects.get(dsc_std=std_reclamo)
            print (estado.std_rec)
            #print (std)
            if estado.std_rec==std_reclamo:
                return False
            if control.exists():
                return False
            
            return True
        
        
def control_tipo_anual(tipo, desde, hasta):
           
           
            if tipo.tipo_anual:
                 
            #     print(tipo_std)
                
                 if desde.day!=1 or  hasta.day!=31:
                    
                     return True
                 
                 if desde.month!=1 or  hasta.month!=12: 
                    
                     return True
                
                
            return False    
                
        