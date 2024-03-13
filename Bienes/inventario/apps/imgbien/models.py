import os
from pathlib import Path
from typing import Iterable, Optional
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils.text import slugify  #genera un slug a partir de una cadena de texto
from inventario.util import unique_slug_generator
from apps.bien.models import Bien
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


def dir_imag(instance, filename):
    return 'Bienes/bien_{0}/{1}'.format(instance.bien.id_bien, filename)  

class ImgBien(models.Model):
    id_img=models.AutoField(primary_key=True)
    img_bien=models.ImageField(upload_to=dir_imag, null=True)
    bien=models.ForeignKey(Bien, on_delete=models.PROTECT, related_name='imagenes')
    user_bien=models.ForeignKey(User, on_delete=models.PROTECT)
    fch_bien=models.DateTimeField(auto_now=True)
    slug=models.SlugField(max_length=200, null=True,blank=True)
    
    def delete(self, *args, **kwargs):
        storage, path = self.img_bien.storage, self.img_bien.path
        # Delete the model before the file
        super(ImgBien, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)
        
    def save(self):
        im = Image.open(self.img_bien)
        output = BytesIO()
        
        
        ancho, alto =im.size
        
        #nalto=300
        #nancho=int((nalto/alto)*ancho)
        nancho=300                                                               
        nalto=300
        im = im.resize( (nancho,nalto) )
        
        im.save(output, format='JPEG', quality=100)
        output.seek(0)
        self.img_bien = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.img_bien.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)
        super(ImgBien,self).save()
		

     
     

        
    
def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        
        val=unique_slug_generator(instance)
        instance.slug=slugify(val)
        
pre_save.connect(slug_generator, sender=ImgBien)


