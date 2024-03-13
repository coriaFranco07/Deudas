from typing import Any
from django import http
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
#------------------------------------------------------------
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, View, DetailView
from django.urls import reverse_lazy
from PIL import Image
from .models import Bien
from apps.imgbien.models import ImgBien
from .forms import BienImgForm
from django.contrib.messages.views import SuccessMessageMixin
# Create your views here.
from PIL import Image


class ListImgBien(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,ListView): 
        model=ImgBien
        template_name='imagenes.html'
        permission_required = "bien.view_bien"
        
        
        def get_context_data(self,**kwargs):
            context = super(ListImgBien, self).get_context_data(**kwargs)
            bien=Bien.objects.get(slug=self.kwargs['slug'])
            context['images']=bien.imagenes.all()
            context['bien']=bien
            
            
            
            #context['bien']=ImgBien.objects.filter(bien=bien_img)
            return context
        
        def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
            return redirect('index')
        
class AddImgBien(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,CreateView): 
    model=ImgBien
    template_name='add_img_img.html'
    permission_required = "imgbien.add_imgbien"
    form_class=BienImgForm
    success_url=reverse_lazy('list_bienes')
    success_message='Imagen Registrada'
        
        
    def form_valid(self, form):
            form.instance.user_bien=self.request.user
            return super().form_valid(form)
   
    """def get(self, request: HttpRequest,slug, *args: str, **kwargs: Any) -> HttpResponse:
          bien=Bien.objects.get(slug=slug)
          initial_data={
              'bien':bien,
              'img_bien': None,
          }
          self.form_class(initial=initial_data)
          return super().get(request, *args, **kwargs)"""
    
    """def get_initial(self):
        bien=Bien.objects.get(slug=self.kwargs['slug'])
        return {'bien': bien}"""
    
    def get_context_data(self,**kwargs):
            context = super(AddImgBien, self).get_context_data(**kwargs)
            bien=Bien.objects.get(slug=self.kwargs['slug'])
            context['bien']=bien
            context['slug']=self.kwargs['slug']
            return context
        
    
    """def get_form_kwargs(self):
        kwargs = super(AddImgBien, self).get_form_kwargs()
        kwargs.update(self.kwargs)  # self.kwargs contains all url conf params
        return kwargs""" 
       
    def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
            return HttpResponseRedirect(reverse_lazy(self.success_url))
        
class RegImgBien(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,CreateView): 
    model=ImgBien
    template_name='add_img_img.html'
    permission_required = "imgbien.add_imgbien"
    form_class=BienImgForm
    success_url=reverse_lazy('list_bienes')
    success_message='Registro editado correctamente'
        
        
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        
        try:
            
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    
                    if request.method=='POST':
                        
                        #bien=Bien.objects.get(slug=request.POST['slug'])   
                        #request.POST['bien'] =bien   
                        #print(request.POST) 
                    #recupero datos del formulario
                        form=BienImgForm(request.POST, request.FILES)
                        #form.bien=bien
                        imag=request.FILES.get('img_bien')
                       
                    if form.is_valid():
                        new_clase=form.save(commit=False)
                        new_clase.bien=Bien.objects.get(slug=request.POST['slug'])
                        new_clase.user_bien=request.user 
                        if imag:
                            with Image.open(imag) as imagen:
                                ancho, alto =imagen.size
                                if ancho > alto:
                                    nalto=300
                                    nancho= int((ancho/alto) * nalto)
                                    imagen.resize=(nancho, nalto) 
                                    imagen.save(imag) 
                                    
                                elif ancho < alto:
                                    nancho=300
                                    nalto=int((alto/ancho)*nancho)
                                    imagen.resize=(nancho, nalto) 
                                    imagen.save(imag) 
                                    
                                else:
                                    imagen.thumbnail((300,300))
                                    imagen.save(imag)
                                  
                            with Image.open(imag) as imagen:
                                ancho, alto =imagen.size
                                if ancho > alto:
                                    left =(ancho-alto)/2
                                    top=0
                                    right=(ancho + alto) /2
                                    bottom=alto

                                else:
                                    left =0
                                    top=(alto - ancho)/2
                                    right= ancho  
                                    bottom=(alto + ancho)/2
                                imagen=imagen.crop((left,top, right, bottom))
                                imagen.save(imag)
                        
                        print(imag.size)
                        #new_clase.img_bien=Image.open(imag).resize(300,300)      
                        
                        new_clase.save()
                        mensaje='Registro Editado Correctamente'
                        error='No hay errores'
                        response=JsonResponse({'mensaje':mensaje, 'error':error})
                        response.status_code=201
                        return response
                    
                    
                        
                    else:
                        
                        mensaje='No se ha podido editar el Registro'
                        
                        error=form.errors
                        response=JsonResponse({'mensaje':mensaje, 'error':error})
                        response.status_code=400
                        return response
                
            else:
               
                return redirect ('list_bienes') 
            
            
            

        except Exception as e:
            
            print(e)
            mensaje='No se ha podido editar el Registro'
            error="e"
            response=JsonResponse({'mensaje':mensaje, 'error':error})
            response.status_code=400
            return response
        
    def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
            return HttpResponseRedirect(reverse_lazy(self.success_url))
        
class DeleteImgBien(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
    model=ImgBien
    #template_name='bienes.html'  
    permission_required = "bien.delete_bien"
    success_url=reverse_lazy('list_bienes')
    raise_exception = True
    
 
    
    def post(self, request,slug, *args, **kwargs) -> HttpResponse:
        
        try:
            clase=ImgBien.objects.get(slug=slug)
            clase.delete()
            messages.add_message(request=request, level=messages.SUCCESS,message='Imagen Eliminada Correctamente') 
            mensaje='Imagen Eliminada'
            error='No hay errores'
            response=JsonResponse({'mensaje':mensaje, 'error':error, 'status_code':201})
            
        except Exception as e:
            
            mensaje='Imagen No Eliminada'
            messages.add_message(request=request, level=messages.ERROR,message='La Imagen No se puede Eliminar') 
            response=JsonResponse({'mensaje':mensaje, 'error':error, 'status_code':400})
        finally:
            
            return response
        
     
    def handle_no_permission(self):
        
        return JsonResponse({'message': 'Acceso Denegado'}, status=401)
        
    
    