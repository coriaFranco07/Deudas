from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
#------------------------------------------------------------
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from .models import Marca
from .forms import MarcaForm
from django.contrib.messages.views import SuccessMessageMixin


    
class ListMarca(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,ListView): 
        model=Marca 
        template_name='marcas.html'
        context_object_name='marcas' 
        permission_required = "marca.view_marca"
        
        def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
            return redirect('index')
    
class AddMarca(LoginRequiredMixin, PermissionRequiredMixin ,SuccessMessageMixin,CreateView):
    model=Marca
    template_name='add_marca.html'
    form_class=MarcaForm
    success_url=reverse_lazy('list_marcas')
    permission_required = "marca.add_marca"
    
   
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        try:
            
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    
                    #recupero datos del formulario
                    form=MarcaForm(data=request.POST)
                    if form.is_valid():
                       
                        new_clase=form.save(commit=False)
                        new_clase.user_marca=request.user  #este es el user que inicio sesion
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
                return redirect ('list_marcas')        
                    
        except Exception as e:
            print('entro en la exeption***********')
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
        

class EditMarca(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
    model=Marca
    template_name='edit_marca.html'
    form_class=MarcaForm
    success_url=reverse_lazy('list_marcas')
    success_message='Registro editado correctamente'
    permission_required = "marca.update_marca"
    
    
    def form_valid(self, form):
            form.instance.user_marca=self.request.user
            return super().form_valid(form)
        
    def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
             #return HttpResponseRedirect(reverse_lazy(self.success_url))
            return JsonResponse({'message': 'Acceso Denegado'}, status=401)

    def post(self, request: HttpRequest,slug, *args: str, **kwargs: Any) -> HttpResponse:
        
        try:
            
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    
                    #recupero datos del formulario
                    form=MarcaForm(data=request.POST, instance=self.get_object())
            
                    if form.is_valid():
                        new_clase=form.save(commit=False)
                        new_clase.user_marca=request.user 
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
               
                return redirect ('list_marcas') 
            
            
            

        except Exception as e:
            print('entro en la exeption***********')
            print(e)
            mensaje='No se ha podido editar el Registro'
            error="e"
            response=JsonResponse({'mensaje':mensaje, 'error':error})
            response.status_code=400
            return response
      
      
class DeleteMarca(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
    model=Marca
    template_name='del_marca.html'  #o crear marca_confirm_delete.html y esta linea se omite
    permission_required = "marca.delete_marca"
    success_url=reverse_lazy('list_marcas')
   
 
    
    def post(self, request,slug, *args, **kwargs) -> HttpResponse:
        try:
            clase=Marca.objects.get(slug=slug)
            clase.delete()
            messages.add_message(request=request, level=messages.SUCCESS,message='Registro Eliminado Correctamente') 
        
        except:
            messages.add_message(request=request, level=messages.ERROR,message='El Registro No se puede Eliminar') 
        
        finally:
            return redirect('list_marcas')
    
    def handle_no_permission(self):
        messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
         #return HttpResponseRedirect(reverse_lazy(self.success_url))
        return JsonResponse({'message': 'Acceso Denegado'}, status=401)