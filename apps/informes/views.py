from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from  apps.deuda.models import Deuda
from datetime import datetime
from django.db.models import Sum,Count, Max, Min
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from apps.reclamo.models import Reclamo
from apps.tipo_reclamo.models import TipoReclamo
from apps.movimiento.models import Movimiento
from apps.lote.models import Lote
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import get_template
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, View
from apps.rec_lote.models import Rec_Lote
from apps.std_mov.models import EstadoMov
from apps.rec_prioridad.models import Rec_Prioridad
from django.urls import reverse_lazy


from django.db.models import Prefetch
 
import operator
from django.db.models import Q

class JSONResponseMixin:
  """
  A mixin that can be used to render a JSON response.
  """
  def render_to_json_response(self, context, **response_kwargs):

    return JsonResponse(self.get_data(context), **response_kwargs)

  def get_data(self, context):

    return context


class InformesView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,View):
  template_name = 'informes.html'
  output_template = get_template('informes.html')
  permission_required = "informes.view_informes"
  success_url=reverse_lazy('index')

  def get(self, request, *args, **kwargs):
    #obj = self.get_object()
    
      try:
    
            rec=Reclamo.objects.filter(std_rec__act_calculo=True)
            #deuda=Deuda.objects.filter(id_rec__std_rec__act_calculo=True)
            deuda = Reclamo.objects.select_related('deudas_reclamos').select_related('prioridad_reclamos').filter(std_rec__act_calculo=True).filter(prioridad_reclamos__orden__gt=0)
                        
            data=[]
          
            for d in deuda:
              
                rec={
                  
                }
              
              
            
            context={
                        
                        'reclamos':deuda,
                        
                    }
                    
            return render(request, self.template_name,context)
          
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
  
class InformesGDEView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,View):
  template_name = 'movs.html'
  output_template = get_template('movs.html')
  permission_required = "informes.view_informes"

  def get(self, request, *args, **kwargs):
    #obj = self.get_object()
    
        try:
    
                #rec=Reclamo.objects.filter(std_rec__act_calculo=True)
                #deuda=Deuda.objects.filter(id_rec__std_rec__act_calculo=True)
                #deuda = Reclamo.objects.select_related('deudas_reclamos').select_related('prioridad_reclamos').filter(std_rec__act_calculo=True).filter(prioridad_reclamos__orden__gt=0)
                movs=Movimiento.objects.prefetch_related(Prefetch('prioridad_movs')).order_by('id_rec')
                
                data=[]     
                for m in movs:
                  
                  np=None
                  for p in m.prioridad_movs.filter(id_mov__pk=m.pk):
                        np=p
                    
                    
                  valor={
                        
                        'movi': m,
                        'prior':np,
                        }
                  
                    
                    
                  data.append(valor)
                    
                
              
                
                
                context={
                            
                            'movs':data,
                            
                        }
                        
                return render(request, self.template_name,context)
              
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