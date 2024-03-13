from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
#------------------------------------------------------------
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from .models import Prioridad, HistPrioridad
from .forms import PrioridadForm
from django.contrib.messages.views import SuccessMessageMixin


    
#class ListPrioridad(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,ListView): 
class ListPrioridad(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,ListView): 
        model=Prioridad
        template_name='prioridades.html'
        context_object_name='prioridades' 
        permission_required = "prioridad.view_prioridad"
        
        def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
            return redirect('index')
    
#class AddPrioridad(LoginRequiredMixin, PermissionRequiredMixin ,SuccessMessageMixin,CreateView):
class AddPrioridad(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,CreateView):
     model=Prioridad
     template_name='add_prioridad.html'
     form_class=PrioridadForm
     success_url=reverse_lazy('list_prioridades')
     permission_required = "prioridad.add_prioridad"
    
   
    
     def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
         try:
            
             if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    
#                     #recupero datos del formulario
                     form=PrioridadForm(data=request.POST)
                     if form.is_valid():
                       
                         new_clase=form.save(commit=False)
                         new_clase.user_prior=request.user  #este es el user que inicio sesion
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
                 return redirect ('list_prioridades')        
                    
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
        


class EditPrioridad(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,UpdateView):        
     model=Prioridad
     template_name='edit_prioridad.html'
     form_class=PrioridadForm
     success_url=reverse_lazy('list_prioridades')
     success_message='Registro editado correctamente'
     permission_required = "prioridad.change_prioridad"
    
    
     def form_valid(self, form):
             form.instance.user_prior=self.request.user
             return super().form_valid(form)
        
     def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
             #return HttpResponseRedirect(reverse_lazy(self.success_url))
            return JsonResponse({'message': 'Acceso Denegado'}, status=401)

     def post(self, request: HttpRequest,slug, *args: str, **kwargs: Any) -> HttpResponse:
        
         try:
            
             if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    
#                     #recupero datos del formulario
                     form=PrioridadForm(data=request.POST, instance=self.get_object())
            
                     if form.is_valid():
                         new_clase=form.save(commit=False)
                         new_clase.user_prior=request.user 
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
               
                 return redirect ('list_prioridades') 
            
            
            

         except Exception as e:
             
             mensaje='No se ha podido editar el Registro'
             error="e"
             response=JsonResponse({'mensaje':mensaje, 'error':error})
             response.status_code=400
             return response
      
      
# class DeleteMarca(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
class DeletePrioridad(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,DeleteView):
     model=Prioridad
     template_name='del_prioridad.html'  #o crear marca_confirm_delete.html y esta linea se omite
     permission_required = "prioridad.delete_prioridad"
     success_url=reverse_lazy('list_prioridades')
   
 
    
     def post(self, request,slug, *args, **kwargs) -> HttpResponse:
         try:
             clase=Prioridad.objects.get(slug=slug)
             
             usuario=request.user
             
             hist_clase= HistPrioridad.objects.create(
                 id_prior=clase.id_prior,
                 dsc_prior=clase.dsc_prior,
                 nivel_prior=clase.nivel_prior,
                 fch_prior=clase.fch_prior,
                 user_prior=clase.user_prior.username,
                 slug=clase.slug,
                 h_user_proc=usuario,
                 h_tipo_proc='D')
             
             clase.delete()
             messages.add_message(request=request, level=messages.SUCCESS,message='Registro Eliminado Correctamente') 
        
         except:
             messages.add_message(request=request, level=messages.ERROR,message='El Registro No se puede Eliminar') 
        
         finally:
             return redirect('list_prioridades')
    
     def handle_no_permission(self):
        messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
         #return HttpResponseRedirect(reverse_lazy(self.success_url))
        return JsonResponse({'message': 'Acceso Denegado'}, status=401)