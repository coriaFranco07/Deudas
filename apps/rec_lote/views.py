from django.shortcuts import render

# Create your views here.
from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
#------------------------------------------------------------
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from .models import Rec_Lote
from apps.rec_prioridad.models import Rec_Prioridad
from apps.reclamo.models import Reclamo
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Prefetch

    
#class ListPrioridad(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,ListView): 
class ListReclamosLotes(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,ListView): 
        model=Reclamo
        template_name='reclamos_lotes.html'
        permission_required = "rec_lote.view_rec_lote"    
        
        
        def get_context_data(self,**kwargs):
            
                try:
                        context = super().get_context_data(**kwargs)
                        rec_lote=Rec_Lote.objects.filter(id_lote__slug=self.kwargs['slug'])
                        
                        lote= []
                        
                       
                       
                        
                        for r in rec_lote:
                            
                            rec_prior= Rec_Prioridad.objects.get(id_rec=r.id_rec)
                            
                            data={
                                
                                'id_legajo': rec_prior.id_rec.id_legajo,
                                'tipo_reclamo': rec_prior.id_rec.id_tipo_rec.dsc_tipo_rec,
                                'fch_dsd':rec_prior.id_rec.fch_dsd_rec,
                                'fch_hst':rec_prior.id_rec.fch_hst_rec,
                                'dias':rec_prior.id_rec.dias_rec,
                                'estado':rec_prior.id_mov.id_std_mov.dsc_std_mov,
                                'orden':rec_prior.orden,
                                'prioridad':rec_prior.id_prior.dsc_prior,
                                'total':rec_prior.id_rec.deudas_reclamos.total
                                
                            }
                            
                            lote.append(data)
                            
                            print(data)
                            
                
            
            
            
                            # rec = Reclamo.objects.prefetch_related(
                            #     Prefetch('lotes_reclamos', queryset=Rec_Lote.objects.filter(id_lote__slug=self.kwargs['slug']))
                            # )#.prefetch_related(Prefetch('prioridad_reclamos', queryset=Rec_Prioridad.objects.all().order_by('orden'))) 
                            
                        
                            # record = Reclamo.objects.all().select_related('prioridad_reclamos').order_by('prioridad_reclamos__orden').prefetch_related( 
                            # Prefetch('lotes_reclamos', queryset=Rec_Lote.objects.filter(id_lote__slug=self.kwargs['slug'])))
                            
                                
                        
                            # for r in rec:
                            #     #for l in r.prioridad_reclamos.all():
                            #         print(r)
                                    
                            
                            #print(rec)
            
                        context={
                                
                                'reclamos':lote,
                                
                        }
                            
                        return  context
                except Exception as e:
                            print('entro en la exeption***********')
                            print(e)
                            mensaje='No se ha podido editar el Registro'
                            error="e"
                            response=JsonResponse({'mensaje':mensaje, 'error':error})
                            response.status_code=400
                            return response
        
        
        
      
        
        def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
            return redirect('index')
    
#class AddPrioridad(LoginRequiredMixin, PermissionRequiredMixin ,SuccessMessageMixin,CreateView):

      
#     def handle_no_permission(self):
#             messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
#              #return HttpResponseRedirect(reverse_lazy(self.success_url))
#             return JsonResponse({'message': 'Acceso Denegado'}, status=401)
        


     