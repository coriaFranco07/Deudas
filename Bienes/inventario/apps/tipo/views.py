from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
#------------------------------------------------------------
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from .models import Tipo
from .forms import TipoForm
from django.contrib.messages.views import SuccessMessageMixin

class ListTipo(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,ListView): 
        model=Tipo 
        template_name='tipos.html'
        context_object_name='tipos'
        permission_required = "tipo.view_tipo"
        
        def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
            return redirect('index')
    
class AddTipo(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,CreateView):
    model=Tipo
    template_name='add_tipo.html'
    form_class=TipoForm
    success_url=reverse_lazy('list_tipos')
    permission_required = "tipo.add_tipo"
    #success_message='Registro creado correctamente'
          
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        try:
            
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    
                    #recupero datos del formulario
                    form=TipoForm(data=request.POST)
                    if form.is_valid():
                       
                        new_clase=form.save(commit=False)
                        new_clase.user_tipo=request.user  #este es el user que inicio sesion
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
                return redirect ('list_tipos')        
                    
        except Exception as e:
           
            print(e)
            mensaje='No se ha podido realizar el Registro'
            error='e'
            response=JsonResponse({'mensaje':mensaje, 'error':error})
            response.status_code=400
            return response
       
    def handle_no_permission(self):
        messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
        return JsonResponse({'message': 'Acceso Denegado'}, status=401)
    
class EditTipo(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
    model=Tipo
    template_name='edit_tipo.html'
    form_class=TipoForm
    success_url=reverse_lazy('list_tipos')
    success_message='Registro editado correctamente'
    permission_required = "tipo.update_tipo"
    
    
    
    def form_valid(self, form):
            form.instance.user_tipo=self.request.user
            return super().form_valid(form)
        
    def post(self, request: HttpRequest,slug, *args: str, **kwargs: Any) -> HttpResponse:
        
        try:
            
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    
                    #recupero datos del formulario
                    form=TipoForm(data=request.POST, instance=self.get_object())
            
                    if form.is_valid():
                        new_clase=form.save(commit=False)
                        new_clase.user_tipo=request.user 
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
               
                return redirect ('list_tipos') 
            
            
            

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
     
class DeleteTipo(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
    model=Tipo
    template_name='del_tipo.html'  #o crear marca_confirm_delete.html y esta linea se omite
    permission_required = "tipo.delete_tipo"
    success_url=reverse_lazy('list_tipos')
    
 
    
    def post(self, request,slug, *args, **kwargs) -> HttpResponse:
        try:
            clase=Tipo.objects.get(slug=slug)
            clase.delete()
            messages.add_message(request=request, level=messages.SUCCESS,message='Registro Eliminado Correctamente') 
        
        except:
            messages.add_message(request=request, level=messages.ERROR,message='El Registro No se puede Eliminar') 
        
        finally:
            return redirect('list_tipos')
    
    def handle_no_permission(self):
        messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
        return JsonResponse({'message': 'Acceso Denegado'}, status=401)