from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
#------------------------------------------------------------
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from .models import EstadoMov, HistEstadoMov
from .forms import EstadoMovForm
from django.contrib.messages.views import SuccessMessageMixin


    
#class ListPrioridad(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,ListView): 
class ListEstMov(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,ListView): 
        model=EstadoMov
        template_name='estados.html'
        context_object_name='estados' 
        permission_required = "std_mov.view_std_mov"
        
        def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
            return redirect('index')
    
#class AddPrioridad(LoginRequiredMixin, PermissionRequiredMixin ,SuccessMessageMixin,CreateView):
class AddEstMov(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,CreateView):
     model=EstadoMov
     template_name='add_estado.html'
     form_class=EstadoMovForm
     success_url=reverse_lazy('list_estados')
     permission_required = "std_mov.add_std_mov"
    
   
    
     def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
         try:
            
             if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    
#                     #recupero datos del formulario
                     form=EstadoMovForm(data=request.POST)
                     if form.is_valid():
                       
                         new_clase=form.save(commit=False)
                         new_clase.user_std_mov=request.user  #este es el user que inicio sesion
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
        

#class EditMarca(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
class EditEstMov(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,UpdateView):        
     model=EstadoMov
     template_name='edit_estado.html'
     form_class=EstadoMovForm
     success_url=reverse_lazy('list_estados')
     success_message='Registro editado correctamente'
     permission_required = "std_mov.change_std_mov"
    
    
     def form_valid(self, form):
             form.instance.user_std_mov=self.request.user
             
             
             return super().form_valid(form)
        
     def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
             #return HttpResponseRedirect(reverse_lazy(self.success_url))
            return JsonResponse({'message': 'Acceso Denegado'}, status=401)

     def post(self, request: HttpRequest,slug, *args: str, **kwargs: Any) -> HttpResponse:
        
         try:
            
             if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    
#                     #recupero datos del formulario
                     form=EstadoMovForm(data=request.POST, instance=self.get_object())
            
                     if form.is_valid():
                         new_clase=form.save(commit=False)
                         new_clase.user_std_mov=request.user 
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
             print('entro en la exeption***********')
             print(e)
             mensaje='No se ha podido editar el Registro'
             error="e"
             response=JsonResponse({'mensaje':mensaje, 'error':error})
             response.status_code=400
             return response
      
      
# class DeleteMarca(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
class DeleteEstMov(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,DeleteView):
     model=EstadoMov
     template_name='del_estado.html'  #o crear marca_confirm_delete.html y esta linea se omite
     permission_required = "std_mov.delete_std_mov"
     success_url=reverse_lazy('list_estados')
   
 
    
     def post(self, request,slug, *args, **kwargs) -> HttpResponse:
         try:
             clase=EstadoMov.objects.get(slug=slug)
             usuario=request.user
             
             hist_clase= HistEstadoMov.objects.create(
                 id_std_mov=clase.id_std_mov,
                 dsc_std_mov=clase.dsc_std_mov,
                 fch_std_mov=clase.fch_std_mov,
                 user_std_mov=clase.user_std_mov.username,
                 slug=clase.slug,
                 h_user_proc=usuario,
                 h_tipo_proc='D')
             
             clase.delete()
             messages.add_message(request=request, level=messages.SUCCESS,message='Registro Eliminado Correctamente') 
        
         except:
             messages.add_message(request=request, level=messages.ERROR,message='El Registro No se puede Eliminar') 
        
         finally:
             return redirect('list_estados')
    
     def handle_no_permission(self):
        messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
         #return HttpResponseRedirect(reverse_lazy(self.success_url))
        return JsonResponse({'message': 'Acceso Denegado'}, status=401)