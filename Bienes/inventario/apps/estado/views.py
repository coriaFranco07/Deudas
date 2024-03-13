from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
#------------------------------------------------------------
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from .models import Estado
from .forms import EstadoForm
from django.contrib.messages.views import SuccessMessageMixin


    
class ListEstado(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,ListView): 
        model=Estado 
        template_name='estados.html'
        context_object_name='estados'
        permission_required = "estado.view_estado" 
        
        def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
            return redirect('index')
    
class AddEstado(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,CreateView):
    model=Estado
    template_name='add_estado.html'
    form_class=EstadoForm
    success_url=reverse_lazy('list_estados')
    permission_required = "estado.add_estado"
    #success_message='Registro creado correctamente'
          
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        try:
            
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    
                    #recupero datos del formulario
                    form=EstadoForm(data=request.POST)
                    if form.is_valid():
                       
                        new_clase=form.save(commit=False)
                        new_clase.user_estado=request.user  #este es el user que inicio sesion
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
                return redirect ('list_estados')        
                    
        except Exception as e:
           
            
            mensaje='No se ha podido realizar el Registro'
            error='e'
            response=JsonResponse({'mensaje':mensaje, 'error':error})
            response.status_code=400
            return response
       
    def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
             #return HttpResponseRedirect(reverse_lazy(self.success_url))
            return JsonResponse({'message': 'Acceso Denegado'}, status=401)

class EditEstado(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
    model=Estado
    template_name='edit_estado.html'
    form_class=EstadoForm
    success_url=reverse_lazy('list_estados')
    success_message='Registro editado correctamente'
    permission_required = "estado.update_estado"
    
    
    
    def form_valid(self, form):
            form.instance.user_estado=self.request.user
            return super().form_valid(form)
        
    def post(self, request: HttpRequest,slug, *args: str, **kwargs: Any) -> HttpResponse:
        
        try:
            
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    
                    #recupero datos del formulario
                    form=EstadoForm(data=request.POST, instance=self.get_object())
            
                    if form.is_valid():
                        new_clase=form.save(commit=False)
                        new_clase.user_estado=request.user 
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
               
                return redirect ('list_estados') 
            
            
            

        except Exception as e:
            
            print(e)
            mensaje='No se ha podido editar el Registro'
            error="e"
            response=JsonResponse({'mensaje':mensaje, 'error':error})
            response.status_code=400
            return response
  
    
    def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
             #return HttpResponseRedirect(reverse_lazy(self.success_url))
            return JsonResponse({'message': 'Acceso Denegado'}, status=401)

class DeleteEstado(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
    model=Estado
    template_name='del_estado.html'  #o crear marca_confirm_delete.html y esta linea se omite
    permission_required = "estado.delete_estado"
    success_url=reverse_lazy('list_estados')
    
    
    def post(self, request,slug, *args, **kwargs) -> HttpResponse:
        try:
            marca=Estado.objects.get(slug=slug)
            marca.delete()
            messages.add_message(request=request, level=messages.SUCCESS,message='Registro Eliminado Correctamente') 
        
        except:
            messages.add_message(request=request, level=messages.ERROR,message='El Registro No se puede Eliminar') 
        
        finally:
            return redirect('list_estados')
    
    def handle_no_permission(self):
        messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
         #return HttpResponseRedirect(reverse_lazy(self.success_url))
        return JsonResponse({'message': 'Acceso Denegado'}, status=401)