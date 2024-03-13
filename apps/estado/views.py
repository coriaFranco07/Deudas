from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
#------------------------------------------------------------
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from .models import Estado, HistEstado
from .forms import EstadoForm
from django.contrib.messages.views import SuccessMessageMixin


    

class ListEstado(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,ListView): 
        model=Estado
        template_name='estados_rec.html'
        context_object_name='estados' 
        permission_required = "estado.view_estado"
        
        def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
            return redirect('index')
    
#class AddPrioridad(LoginRequiredMixin, PermissionRequiredMixin ,SuccessMessageMixin,CreateView):
class AddEstado(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,CreateView):
     model=Estado
     template_name='add_estado_rec.html'
     form_class=EstadoForm
     success_url=reverse_lazy('list_estado_rec')
     permission_required = "estado.add_estado"
    
   
    
     def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
         try:
            
             if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    
#                     #recupero datos del formulario
                     form=EstadoForm(data=request.POST)
                     if form.is_valid():
                       
                         new_clase=form.save(commit=False)
                         new_clase.user_std=request.user  #este es el user que inicio sesion
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
                 return redirect ('list_estado_rec')        
                    
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
            return JsonResponse({'message': 'Acceso Denegado'}, status=403)
        


class EditEstado(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,UpdateView):        
     model=Estado
     template_name='edit_estado_rec.html'
     form_class=EstadoForm
     success_url=reverse_lazy('list_estado_rec')
     success_message='Registro editado correctamente'
     permission_required = "estado.change_estado"
    
     def get(self, request,slug, *args, **kwargs):
        #data=MovData.objects.get(slug=slug)
            try:
                data=Estado.objects.get(slug=slug)
                
                if data.dsc_std=='RECLAMO PAGADO':
                    messages.add_message(request=request, level=messages.ERROR,message='El Estado no puede modificarse') 
                    return  response
        
                return super().get(self)
            
            except Exception as e:
                print('entro en la exeption***********')
                print(e)
                mensaje='No se ha podido editar el Registro'
                error="e"
                response=JsonResponse({'mensaje':mensaje, 'error':error})
                response.status_code=400
                return response
    
     def form_valid(self, form):
             form.instance.user_std=self.request.user
             return super().form_valid(form)
        
     def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
             #return HttpResponseRedirect(reverse_lazy(self.success_url))
            return JsonResponse({'message': 'Acceso Denegado'}, status=401)

     def post(self, request: HttpRequest,slug, *args: str, **kwargs: Any) -> HttpResponse:
        
         try:
            
             if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    
#                     #recupero datos del formulario
                     form=EstadoForm(data=request.POST, instance=self.get_object())
                     
                     if form.is_valid():
                         new_clase=form.save(commit=False)
                         new_clase.user_std=request.user 
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
               
                 return redirect ('list_estado_rec') 
            
            
            

         except Exception as e:
             print('entro en la exeption***********')
             print(e)
             mensaje='No se ha podido editar el Registro'
             error="e"
             response=JsonResponse({'mensaje':mensaje, 'error':error})
             response.status_code=400
             return response
      
      

class DeleteEstado(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,DeleteView):
     model=Estado
     template_name='del_estado_rec.html'  #o crear marca_confirm_delete.html y esta linea se omite
     permission_required = "estado.delete_etado"
     success_url=reverse_lazy('list_estado_rec')
   
     def get(self, request,slug, *args, **kwargs):
        #data=MovData.objects.get(slug=slug)
        
        try:
                data=Estado.objects.get(slug=slug)
                
                if data.dsc_std=='RECLAMO PAGADO':
                    messages.add_message(request=request, level=messages.ERROR,message='El Estado no puede eliminarse') 
                    return  response
        
                return super().get(self)
            
        except Exception as e:
                
                mensaje='No se ha podido editar el Registro'
                error="e"
                response=JsonResponse({'mensaje':mensaje, 'error':error})
                response.status_code=400
                return response
    
     def post(self, request,slug, *args, **kwargs) -> HttpResponse:
         try:
             usuario=request.user
             clase=Estado.objects.get(slug=slug)
             
             usuario=request.user
             
             hist_clase= HistEstado.objects.create(
                 id_std=clase.id_std,
                 dsc_std=clase.dsc_std,
                 act_calculo=clase.act_calculo,
                 permitido=clase.permitido,
                 fch_std=clase.fch_std,
                 user_std=clase.user_std.username,
                 slug_std=clase.slug,
                 h_user_proc=usuario,
                 h_tipo_proc='D')
             
             clase.delete()
             messages.add_message(request=request, level=messages.SUCCESS,message='Registro Eliminado Correctamente') 
        
         except:
             messages.add_message(request=request, level=messages.ERROR,message='El Registro No se puede Eliminar') 
        
         finally:
             return redirect('list_estado_rec')
    
     def handle_no_permission(self):
        messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
         #return HttpResponseRedirect(reverse_lazy(self.success_url))
        return JsonResponse({'message': 'Acceso Denegado'}, status=401)