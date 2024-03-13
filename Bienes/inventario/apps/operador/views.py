from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
#------------------------------------------------------------
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from .models import Operador
from .forms import OperadorForm
from django.contrib.messages.views import SuccessMessageMixin


    
class ListOperador(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,ListView): 
        model=Operador
        template_name='operadores.html'
        context_object_name='operadores' 
        permission_required = "operador.view_operador"
        
        def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
            return redirect('index')
    
class AddOperador(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,CreateView):
    model=Operador
    template_name='add_operador.html'
    form_class=OperadorForm
    success_url=reverse_lazy('list_operadores')
    permission_required = "operador.add_operador"
    
          
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        try:
            
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    
                    #recupero datos del formulario
                    form=OperadorForm(data=request.POST)
                    
                    if form.is_valid():
                        
                        new_clase=form.save(commit=False)
                        new_clase.user_operador=request.user  #este es el user que inicio sesion
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
                return redirect ('list_operadores')        
                    
        except Exception as e:
           
            
            mensaje='No se ha podido realizar el Registro'
            error='e'
            response=JsonResponse({'mensaje':mensaje, 'error':error})
            response.status_code=400
            return response
       
    def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
            return JsonResponse({'message': 'Acceso Denegado'}, status=401)

class EditOperador(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
    model=Operador
    template_name='edit_operador.html'
    form_class=OperadorForm
    success_url=reverse_lazy('list_operadores')
    success_message='Registro editado correctamente'
    permission_required = "operador.change_operador"
    
    
    
    def form_valid(self, form):
            form.instance.user_operador=self.request.user
            return super().form_valid(form)
        
    def handle_no_permission(self):
        messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
        return JsonResponse({'message': 'Acceso Denegado'}, status=401)

class DeleteOperador(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
    model=Operador
    template_name='del_operador.html'  #o crear marca_confirm_delete.html y esta linea se omite
    permission_required = "operador.delete_operador"
    success_url=reverse_lazy('list_operadores')
   
 
    
    def post(self, request,slug, *args, **kwargs) -> HttpResponse:
        try:
            oper=Operador.objects.get(slug=slug)
            oper.delete()
            messages.add_message(request=request, level=messages.SUCCESS,message='Registro Eliminado Correctamente') 
        
        except:
            messages.add_message(request=request, level=messages.ERROR,message='El Registro No se puede Eliminar') 
        
        finally:
            return redirect('list_operadores')
    
    def handle_no_permission(self):
        messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
        return JsonResponse({'message': 'Acceso Denegado'}, status=401)