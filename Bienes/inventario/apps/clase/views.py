from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse,HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
#------------------------------------------------------------
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from .models import Clase
from .forms import ClaseForm
from django.contrib.messages.views import SuccessMessageMixin


    
class ListClase(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,ListView): 
        model=Clase
        template_name='clases.html'
        context_object_name='clases'
        permission_required = "clase.view_clase"
        
        
        def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
            return redirect('index')
    
class AddClase(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,CreateView):
    model=Clase
    template_name='add_clase.html'
    form_class=ClaseForm
    success_url=reverse_lazy('list_clases')
    permission_required = "clase.add_clase"
    #success_message='Registro creado correctamente'
    raise_exception = True
          
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        try:
            
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    
                    #recupero datos del formulario
                    form=ClaseForm(data=request.POST)
                    if form.is_valid():
                       
                        new_clase=form.save(commit=False)
                        new_clase.user_clase=request.user  #este es el user que inicio sesion
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
                return redirect ('list_clases')        
                    
        except Exception as e:
           
            print(e)
            mensaje='No se ha podido realizar el Registro'
            error='e'
            response=JsonResponse({'mensaje':mensaje, 'error':error})
            response.status_code=400
            return response
       
    def handle_no_permission(self):
           
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
            #return HttpResponseRedirect(reverse_lazy(self.success_url))
            return JsonResponse({'message': 'Acceso Denegado'}, status=401)
         
class EditClase(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
    model=Clase
    template_name='edit_clase.html'
    form_class=ClaseForm
    success_url=reverse_lazy('list_clases')
    success_message='Registro editado correctamente'
    permission_required = "clase.update_clase"
    
    
    
    def form_valid(self, form):
            form.instance.user_clase=self.request.user
            return super().form_valid(form)
        
    def post(self, request: HttpRequest,slug, *args: str, **kwargs: Any) -> HttpResponse:
        
        try:
            
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    
                    #recupero datos del formulario
                    form=ClaseForm(data=request.POST, instance=self.get_object())
            
                    if form.is_valid():
                        new_clase=form.save(commit=False)
                        new_clase.user_clase=request.user 
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
               
                return redirect ('list_clases') 
            
            
            

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
             
class DeleteClase(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
    model=Clase
    template_name='del_clase.html'  
    permission_required = "clase.delete_clase"
    success_url=reverse_lazy('list_clases')
    
 
    
    def post(self, request,slug, *args, **kwargs) -> HttpResponse:
       
        try:
            clase=Clase.objects.get(slug=slug)
            clase.delete()
            messages.add_message(request=request, level=messages.SUCCESS,message='Registro Eliminado Correctamente') 
        
        except Exception as e:
            
            messages.add_message(request=request, level=messages.ERROR,message='El Registro No se puede Eliminar') 
        
        finally:
            return redirect('list_clases')
    
    def handle_no_permission(self):
        messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
        #return HttpResponseRedirect(self.success_url)
        return JsonResponse({'message': 'Acceso Denegado'}, status=401)
    
