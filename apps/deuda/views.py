from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
#------------------------------------------------------------
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from .models import Deuda
from .forms import DeudaForm
from apps.reclamo.models import Reclamo
from django.contrib.messages.views import SuccessMessageMixin
from apps.movimiento.models import Movimiento
from apps.prioridad.models import Prioridad
from apps.lote.verif_reclamo import Verif_Lotes



    

class EditDeuda(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,UpdateView):        
     model=Deuda
     template_name='edit_rec_deuda.html'
     
     form_class=DeudaForm
     #queryset = Rec_Prioridad.objects.all()
     success_url=reverse_lazy('list_reclamos')
     success_message='Registro editado correctamente'
     permission_required = "deuda.change_deuda"
     
    
     
    
     def form_valid(self, form):
             form.instance.user_deudar=self.request.user
             return super().form_valid(form)
        
     def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
             #return HttpResponseRedirect(reverse_lazy(self.success_url))
            return JsonResponse({'message': 'Acceso Denegado'}, status=401)

     def post(self, request: HttpRequest,slug, *args: str, **kwargs: Any) -> HttpResponse:
        
        try:
            
             if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                     verif = Verif_Lotes()
                     
#                     #recupero datos del formulario
                     form=DeudaForm(data=request.POST, instance=self.get_object())
                     rec=Deuda.objects.get(slug=slug)
                     if verif.rec_in_lote(rec.id_rec.slug):
                         mensaje='No se puede modificar la deuda'
                        
                         error=['Reclamo en lote cerrado']
                         response=JsonResponse({'mensaje':mensaje, 'error':error})
                         response.status_code=400
                         return response
                    
                     elif form.is_valid():
                         new_clase=form.save(commit=False)
                         new_clase.user_deuda=request.user 
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
               
                 return redirect ('list_reclamos') 
            
            
            

        except Exception as e:
             
             mensaje='No se ha podido editar el Registro'
             error="e"
             response=JsonResponse({'mensaje':mensaje, 'error':error})
             response.status_code=400
             return response