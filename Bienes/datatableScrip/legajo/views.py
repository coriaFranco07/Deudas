from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
#------------------------------------------------------------
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from .models import Legajo, HistLegajo
from .forms import LegajoForm
from django.contrib.messages.views import SuccessMessageMixin


    
#class ListPrioridad(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,ListView): 
class ListLegajo(ListView): 
        model=Legajo
        template_name='legajos.html'
        context_object_name='legajos' 
        #permission_required = "prioridad.view_prioridad"
        
        # def handle_no_permission(self):
        #     messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
        #     return redirect('index')
    
#class AddPrioridad(LoginRequiredMixin, PermissionRequiredMixin ,SuccessMessageMixin,CreateView):
class AddLegajo(SuccessMessageMixin,CreateView):
     model=Legajo
     template_name='add_legajo.html'
     form_class=LegajoForm
     success_url=reverse_lazy('list_legajos')
#     permission_required = "marca.add_marca"
    
   
    
     def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
         try:
            
             if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    
#                     #recupero datos del formulario
                     form=LegajoForm(data=request.POST)
                     if form.is_valid():
                       
                         new_clase=form.save(commit=False)
                         new_clase.user_leg=request.user  #este es el user que inicio sesion
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
                 return redirect ('list_legajos')        
                    
         except Exception as e:
             print('entro en la exeption***********')
             print(e)
             mensaje='No se ha podido realizar el Registro'
             error='e'
             response=JsonResponse({'mensaje':mensaje, 'error':error})
             response.status_code=400
             return response
      
#     def handle_no_permission(self):
#             messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
#              #return HttpResponseRedirect(reverse_lazy(self.success_url))
#             return JsonResponse({'message': 'Acceso Denegado'}, status=401)
        

#class EditMarca(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
class EditLegajo(SuccessMessageMixin,UpdateView):        
     model=Legajo
     template_name='edit_legajo.html'
     form_class=LegajoForm
     success_url=reverse_lazy('list_legajos')
     success_message='Registro editado correctamente'
#     permission_required = "marca.update_marca"
    
    
     def form_valid(self, form):
             form.instance.user_leg=self.request.user
             return super().form_valid(form)
        
#     def handle_no_permission(self):
#             messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
#              #return HttpResponseRedirect(reverse_lazy(self.success_url))
#             return JsonResponse({'message': 'Acceso Denegado'}, status=401)

     def post(self, request: HttpRequest,slug, *args: str, **kwargs: Any) -> HttpResponse:
        
         try:
            
             if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    
#                     #recupero datos del formulario
                     form=LegajoForm(data=request.POST, instance=self.get_object())
                     
                     if form.is_valid():
                         new_clase=form.save(commit=False)
                         new_clase.user_leg=request.user 
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
               
                 return redirect ('list_legajos') 
            
            
            

         except Exception as e:
             print('entro en la exeption***********')
             print(e)
             mensaje='No se ha podido editar el Registro'
             error="e"
             response=JsonResponse({'mensaje':mensaje, 'error':error})
             response.status_code=400
             return response
      
      
# class DeleteMarca(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
class DeleteLegajo(SuccessMessageMixin,DeleteView):
     model=Legajo
     template_name='del_legajo.html'  #o crear marca_confirm_delete.html y esta linea se omite
#     permission_required = "marca.delete_marca"
     success_url=reverse_lazy('list_legajos')
   
 
    
     def post(self, request,slug, *args, **kwargs) -> HttpResponse:
         try:
             usuario=request.user
             clase=Legajo.objects.get(slug=slug)
            
             print(clase.slug)
             usuario=request.user
             
             hist_clase= HistLegajo.objects.create(
                 id_legajo=clase.id_legajo,
                 #nro_doc=clase.nro_doc,
                 nombres=clase.nombres,
                 jerarquia=clase.jerarquia,
                 cuerpo=clase.cuerpo,
                 fch_leg=clase.fch_leg,
                 user_leg=clase.user_leg.username,
                 slug=clase.slug,
                 h_user_proc=usuario,
                 h_tipo_proc='D')
             
             clase.delete()
             messages.add_message(request=request, level=messages.SUCCESS,message='Registro Eliminado Correctamente') 
        
         except:
             messages.add_message(request=request, level=messages.ERROR,message='El Registro No se puede Eliminar') 
        
         finally:
             return redirect('list_legajos')
    
#     def handle_no_permission(self):
#         messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
#          #return HttpResponseRedirect(reverse_lazy(self.success_url))
#         return JsonResponse({'message': 'Acceso Denegado'}, status=401)