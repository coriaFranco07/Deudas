from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
#------------------------------------------------------------
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from .models import ControlEstado, HistControlEstado
from .forms import ControlEstadoForm
from django.contrib.messages.views import SuccessMessageMixin
 

class ListControlEstado(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,ListView): 
        model=ControlEstado
        template_name='controles_std.html'
        context_object_name='controles' 
        permission_required = "control_std.view_control_std"
        
        def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
            return redirect('index')
    

class AddControlEstado(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,CreateView):
     model=ControlEstado
     template_name='add_control_std.html'
     form_class=ControlEstadoForm
     success_url=reverse_lazy('list_controles_std')
     permission_required = "control_std.add_control_std"
    
   
    
     def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
         try:
            
             if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    
#                     #recupero datos del formulario
                     form=ControlEstadoForm(data=request.POST)
                     if form.is_valid():
                       
                         new_clase=form.save(commit=False)
                         new_clase.user_control_std=request.user  #este es el user que inicio sesion
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
                 return redirect ('list_controles_std')        
                    
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
        


class EditControlEstado(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,UpdateView):        
     model=ControlEstado
     template_name='edit_control_std.html'
     form_class=ControlEstadoForm
     success_url=reverse_lazy('list_controles_std')
     success_message='Registro editado correctamente'
     permission_required = "control_std.change_control_std"
    
    
     def form_valid(self, form):
             form.instance.user_control_std=self.request.user
             return super().form_valid(form)
        
     def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
             #return HttpResponseRedirect(reverse_lazy(self.success_url))
            return JsonResponse({'message': 'Acceso Denegado'}, status=401)

     def post(self, request: HttpRequest,slug, *args: str, **kwargs: Any) -> HttpResponse:
        
         try:
            
             if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    
#                     #recupero datos del formulario
                     form=ControlEstadoForm(data=request.POST, instance=self.get_object())
            
                     if form.is_valid():
                         new_clase=form.save(commit=False)
                         new_clase.user_control_std=request.user 
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
               
                 return redirect ('list_controles_std') 
            
            
            

         except Exception as e:
             print('entro en la exeption***********')
             print(e)
             mensaje='No se ha podido editar el Registro'
             error="e"
             response=JsonResponse({'mensaje':mensaje, 'error':error})
             response.status_code=400
             return response
      
      

class DeleteControlEstado(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
    model=ControlEstado
    template_name='del_control_std.html'  #o crear marca_confirm_delete.html y esta linea se omite
    permission_required = "control_std.delete_control_std"
    success_url=reverse_lazy('list_controles_std')
   
 
    
    def post(self, request,slug, *args, **kwargs) -> HttpResponse:
         try:
             usuario=request.user
             
             clase=ControlEstado.objects.get(slug=slug)
            
            
             
             hist_clase= HistControlEstado.objects.create(
                 id_contro_std=clase.id_contro_std,
                 std_origen=clase.std_origen.dsc_std,
                 std_destino=clase.std_destino.dsc_std,
                 fch_control_std=clase.fch_control_std,
                 
                 user_control_std=clase.user_control_std.username,
                 slug_std=clase.slug,
                 h_user_proc=usuario,
                 h_tipo_proc='D')
            
             clase.delete()
             
             
             
             
             messages.add_message(request=request, level=messages.SUCCESS,message='Registro Eliminado Correctamente') 
        
         except:
             messages.add_message(request=request, level=messages.ERROR,message='El Registro No se puede Eliminar') 
        
         finally:
             return redirect('list_controles_std')
    
    def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
            
            return JsonResponse({'message': 'Acceso Denegado'}, status=401)