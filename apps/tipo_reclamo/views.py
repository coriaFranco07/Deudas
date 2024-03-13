from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
#------------------------------------------------------------
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from .models import TipoReclamo, HistTipoReclamo
from .forms import TipoRecForm
from django.contrib.messages.views import SuccessMessageMixin


    
#class ListPrioridad(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,ListView): 
class ListTipoeRec(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,ListView): 
        model=TipoReclamo
        template_name='tipos_reclamos.html'
        context_object_name='tipos' 
        permission_required = "tipo_reclamo.view_tipo_reclamo"
        
        def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
            return redirect('index')
    
#class AddPrioridad(LoginRequiredMixin, PermissionRequiredMixin ,SuccessMessageMixin,CreateView):
class AddTipoRec(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,CreateView):
     model=TipoReclamo
     template_name='add_tipo_rec.html'
     form_class=TipoRecForm
     success_url=reverse_lazy('list_tipos_rec')
     permission_required = "tipo_reclamo.add_tipo_reclamo"
    
   
    
     def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
         try:
            
             if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    
#                     #recupero datos del formulario
                     form=TipoRecForm(data=request.POST)
                     if form.is_valid():
                       
                         new_clase=form.save(commit=False)
                         new_clase.user_tipo_rec=request.user  #este es el user que inicio sesion
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
                 return redirect ('list_tipos_rec')        
                    
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
        

#class EditMarca(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
class EditTipoRec(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,UpdateView):        
     model=TipoReclamo
     template_name='edit_tipo_rec.html'
     form_class=TipoRecForm
     success_url=reverse_lazy('list_tipos_rec')
     success_message='Registro editado correctamente'
     permission_required = "tipo_reclamo.change_tipo_reclamo"
    
    
     def form_valid(self, form):
             form.instance.user_tipo_rec=self.request.user
             return super().form_valid(form)
        
     def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
             #return HttpResponseRedirect(reverse_lazy(self.success_url))
            return JsonResponse({'message': 'Acceso Denegado'}, status=401)

     def post(self, request: HttpRequest,slug, *args: str, **kwargs: Any) -> HttpResponse:
        
         try:
            
             if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    
#                     #recupero datos del formulario
                     form=TipoRecForm(data=request.POST, instance=self.get_object())
            
                     if form.is_valid():
                         new_clase=form.save(commit=False)
                         new_clase.user_tipo_rec=request.user 
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
               
                 return redirect ('list_tipos_rec') 
            
            
            

         except Exception as e:
             print('entro en la exeption***********')
             print(e)
             mensaje='No se ha podido editar el Registro'
             error="e"
             response=JsonResponse({'mensaje':mensaje, 'error':error})
             response.status_code=400
             return response
      
      
# class DeleteMarca(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
class DeleteTipoRec(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,DeleteView):
     model=TipoReclamo
     template_name='del_tipo_rec.html'  #o crear marca_confirm_delete.html y esta linea se omite
     permission_required = "tipo_reclamo.delete_tipo_reclamo"
     success_url=reverse_lazy('list_tipos_rec')
   
 
    
     def post(self, request,slug, *args, **kwargs) -> HttpResponse:
         try:
             clase=TipoReclamo.objects.get(slug=slug)
             
             usuario=request.user
             
             hist_clase= HistTipoReclamo.objects.create(
                 id_tipo_rec=clase.id_tipo_rec,
                 codigo_rec=clase.codigo_rec,
                 dsc_tipo_rec=clase.dsc_tipo_rec,
                 tipo_anual=clase.tipo_anual,
                 fch_tipo_rec=clase.fch_tipo_rec,
                 user_tipo_rec=clase.user_tipo_rec.username,
                 slug=clase.slug,
                 h_user_proc=usuario,
                 h_tipo_proc='D')
             
             clase.delete()
             messages.add_message(request=request, level=messages.SUCCESS,message='Registro Eliminado Correctamente') 
        
         except:
             messages.add_message(request=request, level=messages.ERROR,message='El Registro No se puede Eliminar') 
                                             
         finally:
             return redirect('list_tipos_rec')
    
     def handle_no_permission(self):
        messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
         #return HttpResponseRedirect(reverse_lazy(self.success_url))
        return JsonResponse({'message': 'Acceso Denegado'}, status=401)