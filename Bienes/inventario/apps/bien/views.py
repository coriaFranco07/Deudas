from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
#------------------------------------------------------------
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, View, DetailView
from django.urls import reverse_lazy
from .models import Bien
from apps.imgbien.models import ImgBien
from .forms import BienForm
from django.contrib.messages.views import SuccessMessageMixin
  
class ListBien(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,ListView): 
        model=Bien
        template_name='bienes.html'
        context_object_name='bienes'
        permission_required = "bien.view_bien"
        
        def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
            return redirect('index') 
    
class AddBien(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,CreateView):
    model=Bien
    template_name='add_bien.html'
    form_class=BienForm
    success_url=reverse_lazy('list_bienes')
    permission_required = "bien.add_bien"
    
    
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        try:
            print(request.POST)
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    
                    #recupero datos del formulario
                    form=BienForm(data=request.POST)
                    if form.is_valid():
                       
                        new_clase=form.save(commit=False)
                        new_clase.user_bien=request.user  #este es el user que inicio sesion
                        new_clase.save()
                        mensaje='Registro Credado Correctamente'
                        error='No hay errores'
                        response=JsonResponse({'mensaje':mensaje, 'error':error})
                        response.status_code=201
                        return response
                    
                    
                        
                    else:
                        
                        mensaje='No se ha podido realizar el Registro'
                        
                        error=form.errors
                        response=JsonResponse({'mensaje':mensaje, 'error':error})
                        response.status_code=400
                        return response
            
            
            
            else:
                return redirect (self.success_url)        
                    
        except Exception as e:
           
            print(e)
            mensaje='No se ha podido realizar el Registro'
            error='e'
            response=JsonResponse({'mensaje':mensaje, 'error':error})
            response.status_code=400
            return response
       
    def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
            return HttpResponseRedirect(reverse_lazy(self.success_url)) 
            
class EditBien(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
    model=Bien
    template_name='edit_bien.html'
    form_class=BienForm
    success_url=reverse_lazy('list_bienes')
    success_message='Registro editado correctamente'
    permission_required = "bien.change_bien"
    
    
    
    def form_valid(self, form):
            form.instance.user_bien=self.request.user
            return super().form_valid(form)
        
    
    def post(self, request: HttpRequest,slug, *args: str, **kwargs: Any) -> HttpResponse:
        
        try:
            
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    
                    #recupero datos del formulario
                    form=BienForm(data=request.POST, instance=self.get_object())
            
                    if form.is_valid():
                        new_clase=form.save(commit=False)
                        new_clase.user_bien=request.user 
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
            
class DeleteBien(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
    model=Bien
    template_name='del_bien.html'  #o crear marca_confirm_delete.html y esta linea se omite
    permission_required = "bien.delete_bien"
    permission_denied_message="Acceso Denegado"
    success_url=reverse_lazy('list_bienes')
   
    
    def post(self, request,slug, *args, **kwargs) -> HttpResponse:
        try:
            bien=Bien.objects.get(slug=slug)
            bien.delete()
            messages.add_message(request=request, level=messages.SUCCESS,message='Registro Eliminado Correctamente') 
        
        except:
            messages.add_message(request=request, level=messages.ERROR,message='El Registro No se puede Eliminar') 
        
        finally:
            return redirect('list_bienes')
    
    def handle_no_permission(self):
        messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
        return HttpResponseRedirect(reverse_lazy(self.success_url))
    
   

        
      