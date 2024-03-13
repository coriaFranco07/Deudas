from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
#------------------------------------------------------------
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from .models import Oficina
from .forms import OficinaForm
from django.contrib.messages.views import SuccessMessageMixin


    
class ListOficina(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,ListView): 
        model=Oficina 
        template_name='oficinas.html'
        context_object_name='oficinas' 
        permission_required = "oficina.view_oficina"
        
        
        def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
            return redirect('index')
    
class AddOficina(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,CreateView):
    model=Oficina
    template_name='add_oficina.html'
    form_class=OficinaForm
    success_url=reverse_lazy('list_oficinas')
    permission_required = "oficina.add_oficina"
    #success_message='Registro creado correctamente'
          
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        try:
            
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    
                    #recupero datos del formulario
                    form=OficinaForm(data=request.POST)
                    
                    if form.is_valid():
                        
                        new_clase=form.save(commit=False)
                        new_clase.user_oficina=request.user  #este es el user que inicio sesion
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
                
                return redirect ('list_oficinas')        
                    
        except Exception as e:
            
            
            mensaje='No se ha podido realizar el Registro'
            error= form.errors
            response=JsonResponse({'mensaje':mensaje, 'error':error})
            response.status_code=400
            return response
      
    def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
            return JsonResponse({'message': 'Acceso Denegado'}, status=401) 
           
class EditOficina(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
    model=Oficina
    template_name='edit_oficina.html'
    form_class=OficinaForm
    success_url=reverse_lazy('list_oficinas')
    success_message='Registro editado correctamente'
    permission_required = "oficina.update_oficina"
    
    
    
    def form_valid(self, form):
            form.instance.user_oficina=self.request.user
            return super().form_valid(form)
        
    def post(self, request: HttpRequest,slug, *args: str, **kwargs: Any) -> HttpResponse:
        
        try:
            
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    
                    #recupero datos del formulario
                    form=OficinaForm(data=request.POST, instance=self.get_object())
            
                    if form.is_valid():
                        new_clase=form.save(commit=False)
                        new_clase.user_oficina=request.user 
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
               
                return redirect ('list_oficinas') 
            
            
            

        except Exception as e:
            
            print(e)
            mensaje='No se ha podido editar el Registro'
            error="e"
            response=JsonResponse({'mensaje':mensaje, 'error':error})
            response.status_code=400
            return response
         
    def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
            return JsonResponse({'message': 'Acceso Denegado'}, status=401) 

class DeleteOficina(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
    model=Oficina
    template_name='del_oficina.html'  #o crear marca_confirm_delete.html y esta linea se omite
    permission_required = "oficina.delete_oficina"
    success_url=reverse_lazy('list_oficinas')
    
 
    
    def post(self, request,slug, *args, **kwargs) -> HttpResponse:
        try:
            clase=Oficina.objects.get(slug=slug)
            clase.delete()
            messages.add_message(request=request, level=messages.SUCCESS,message='Registro Eliminado Correctamente') 
        
        except:
            messages.add_message(request=request, level=messages.ERROR,message='El Registro No se puede Eliminar') 
        
        finally:
            return redirect('list_oficinas')
    
    def handle_no_permission(self):
        messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
        return JsonResponse({'message': 'Acceso Denegado'}, status=401)