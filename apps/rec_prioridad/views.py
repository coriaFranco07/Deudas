from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
#------------------------------------------------------------
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from .models import Rec_Prioridad
from .forms import RecPrioridadForm
from apps.reclamo.models import Reclamo
from django.contrib.messages.views import SuccessMessageMixin
from apps.movimiento.models import Movimiento
from apps.prioridad.models import Prioridad
from .orden import Orden
from apps.estado.models import Estado


    

class EditPrioridad(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,UpdateView):        
     model=Rec_Prioridad
     template_name='edit_rec_prior.html'
     
     form_class=RecPrioridadForm
     #queryset = Rec_Prioridad.objects.all()
     #success_url=reverse_lazy('list_prioridades')
     success_message='Registro editado correctamente'
     permission_required = "rec_prioridad.change_rec_prioridad"
     
    
     
    #  def get_form_kwargs(self):
    #      kwargs = super().get_form_kwargs()
    #      slug_mov =self.kwargs['slug_mov']
    #      slug_rec_prior=self.kwargs['slug']
    #      kwargs.update({ 'slug_mov':slug_mov, 'slug_rec_prior':slug_rec_prior})
    #      return kwargs
    
     def get_context_data(self, **kwargs):
       
        context = super().get_context_data(**kwargs)
        slug_mov=self.kwargs.get('slug_mov')
        
        slug_prior = self.kwargs.get('slug')
        pr=Rec_Prioridad.objects.get(slug=slug_prior)
        form=RecPrioridadForm(instance=pr)
        context['slug_mov'] = slug_mov
        context['slug_prior'] = slug_prior
        context['form'] = form
       
        return context
    
     def form_valid(self, form):
             form.instance.user_rec_prior=self.request.user
             return super().form_valid(form)
        
     def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
             #return HttpResponseRedirect(reverse_lazy(self.success_url))
            return JsonResponse({'message': 'Acceso Denegado'}, status=401)

     def post(self, request: HttpRequest,slug,slug_mov, *args: str, **kwargs: Any) -> HttpResponse:
        
         try:
            
             if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                     
                     movim=Movimiento.objects.get(slug=slug_mov)
                     prior=Rec_Prioridad.objects.get(slug=slug)
                     slug_rec=prior.id_rec.slug
                     
                     new_prior=request.POST.get('id_prior',"")
                     val_prior= Prioridad.objects.get(pk=new_prior)
                     old_prior=prior.id_prior
                     new_norma_prior=request.POST.get('norma_legal_prior',"")
                     old_norma_pior=prior.norma_legal_prior
                     
                     estado=Estado.objects.get(id_std=prior.id_rec.std_rec.id_std)
                                        
                                        
#                     #recupero datos del formulario
                     #form=RecPrioridadForm(data=request.POST, initial={'id_mov':mov, 'id_rec':reclamo})
                     form = RecPrioridadForm(request.POST)
                     
                     
                     if form.is_valid():
                         
                         
                         
                        
                         #print(f'old: {old_prior} - new: {val_prior}')
                         if not estado.act_calculo:
                            mensaje='No se ha podido editar el Registro'
                        
                            error=["Estado Reclamo: " + estado.dsc_std]
                            response=JsonResponse({'mensaje':mensaje, 'error':error})
                            response.status_code=400
                            return response
                             
                         elif old_prior != val_prior or old_norma_pior != new_norma_prior:
                             updateprior=Rec_Prioridad.objects.filter(slug=slug).update(id_prior=new_prior, id_mov=movim,user_rec_prior=request.user, fch_orden=movim.fch_std_mov, norma_legal_prior=new_norma_prior)
                             orden=Orden()
                             orden.recalc_prior(request.user, timezone.datetime.today())
                             mensaje='Edición Correcta, Los Ordenes se recalcularon'
                         else:
                             mensaje='No se realizaron cambios'
                             
                         
                         
                             
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
               
                  return redirect ('list_detalles' , slug_rec) 
            
            
            

         except Exception as e:
             print('entro en la exeption***********')
             print(e)
             mensaje='No se ha podido editar el Registro'
             error="e"
             response=JsonResponse({'mensaje':mensaje, 'error':error})
             response.status_code=400
             return response
      
