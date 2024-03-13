from django import forms
from .models import ImgBien
from apps.bien.models import Bien
        


img_bien=forms.ClearableFileInput()


class BienImgForm(forms.ModelForm): 
    class Meta:
        model=ImgBien
        fields=['img_bien']
        labels={
            'img_bien': 'Nueva Imagen'
        }
        exclude= ('bienr', )
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
        self.fields["img_bien"].widget.attrs.update(
                {
                
                    'class':"drop-zoon__file-input" ,
                    'name':"img_bien" ,
                    'id':"img_bien" ,
                    'accept':"image/*" ,
                    
                }
            )
        """self.fields["bien"].widget.attrs.update(
                {
                
                    'class':"form-control" ,
                    'name':"bien" ,
                    'id':"bien" ,

                }
            )
      
        self.fields['bien'].widget.attrs['readonly'] = True"""