
from django import forms
from .models import Oficina


class OficinaForm(forms.ModelForm):
    id_oficina=forms.IntegerField(min_value=1)
    dsc_oficina=forms.CharField(min_length=3, max_length=50)
    id_oficina_padre=forms.ModelChoiceField(queryset=Oficina.objects.all())
    
    #id_oficina_padre=forms.IntegerField(min_value=1)
    class Meta:
        model=Oficina
        fields=['id_oficina','dsc_oficina','id_oficina_padre']
        
        
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["id_oficina"].widget.attrs.update({"class": "form-control", 'autofocus':True})
        self.fields["dsc_oficina"].widget.attrs.update({"class": "form-control text-center"})
        self.fields["id_oficina_padre"].widget.attrs.update(
            {
                'data-dropdown-parent':'#ofi_card',
                'class':"form-control" ,
                'name':"id_oficina_padre" ,
                'id':"id_oficina_padre" ,
                'title':"id_oficina_padre" ,
                'style':"width: 100%", 
            }
        )
            
        if self.instance.slug:
            self.fields['id_oficina'].widget.attrs['readonly'] = True
            self.fields['id_oficina'].widget.attrs.update({'class': 'form-control center' })
            
            self.fields["dsc_oficina"].widget.attrs.update({"class": "form-control", 'autofocus':True})
            self.fields["id_oficina_padre"].widget.attrs.update(
                {
                    'data-dropdown-parent':'#ofi_card',
                    'class':"form-control" ,
                    'name':"id_oficina_padre" ,
                    'id':"id_oficina_padre" ,
                    'title':"id_oficina_padre" ,
                    'style':"width: 100%",
                }
            )

    
    def clean(self) -> None:
            
            
            ofi_data_id=self.cleaned_data['id_oficina']
            
            ofi=Oficina.objects.filter(id_oficina=ofi_data_id)
            
            
            if not self.cleaned_data['dsc_oficina']:
                raise forms.ValidationError('Ingrese Descripción')
            ofi_data_desc=self.cleaned_data['dsc_oficina']
            
            buscar=Oficina.objects.filter(dsc_oficina__iexact=ofi_data_desc)
           
            ofi_data_padre_id=self.cleaned_data['id_oficina_padre']
            
            if self.instance.slug:
                ofi_orig= Oficina.objects.get(slug=self.instance.slug)
                
                if ofi_orig.id_oficina != ofi_data_id:
                    raise forms.ValidationError('Codigo Oficina Modificado')
                
                if ofi_orig.id_oficina != ofi_data_id:
                    if ofi:
                        raise forms.ValidationError('El Codigo Existe')
                if ofi_orig.dsc_oficina != ofi_data_desc:   
                    if buscar:
                        raise forms.ValidationError('La Dependencia Existe')
            
            else:
                if ofi:
                    raise forms.ValidationError('El Codigo Existe ')
                if buscar:
                    raise forms.ValidationError('La Dependencia Existe')
            
            if ofi_data_padre_id.id_oficina==ofi_data_id:
                    raise forms.ValidationError('Dependencia y Superior deben ser distintos')    
            
            if not ofi_data_padre_id:             
                    raise forms.ValidationError('Ingrese Dependencia Superior')  
                
            
            if not ofi_data_padre_id==1:
                try:
                    result=[]
                    valor=oficinas_user( ofi_data_padre_id.id_oficina, result,ofi_data_id)
                    return super().clean()
                except:
                    raise forms.ValidationError('Verifique Oficina Padre, genera Bucle infinito')

            return self.cleaned_data
        
                
def oficinas_user(id_oficina,result, ofi_id):
    if id_oficina==ofi_id:
                raise  Exception
    
    result.append(id_oficina)
    oficina = Oficina.objects.filter(id_oficina=id_oficina)
    
    if oficina:
        for of in oficina:
            if not of.id_oficina_padre.id_oficina == 1:
                resultado = oficinas_user(of.id_oficina_padre.id_oficina, result, ofi_id)
    return result

   