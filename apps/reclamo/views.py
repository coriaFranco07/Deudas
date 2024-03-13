from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
#------------------------------------------------------------
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from .models import Reclamo, HistReclamo
from .forms import ReclamoForm, SuplForm
from apps.rec_prioridad.models import Rec_Prioridad
from apps.prioridad.models import Prioridad
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Avg, Max, Min, Sum
from apps.std_mov.models import EstadoMov
from apps.movimiento.models import Movimiento
from apps.deuda.models import Deuda
from apps.rec_lote.models import Rec_Lote
from apps.lote.verif_reclamo import Verif_Lotes
from apps.lote.lotes import Calc_Lotes
from apps.rec_prioridad.orden import Orden



def index(request):
    return render (request, 'indexbase.html')
    
#class ListPrioridad(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,ListView): 
class ListReclamos(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,ListView): 
        model=Reclamo
        template_name='reclamos.html'
        #context_object_name='reclamos' 
        #queryset = Reclamo.objects.filter(activo_rec=False)
        permission_required = "reclamo.view_reclamo"
        
        def get_context_data(self,**kwargs):
            context = super().get_context_data(**kwargs)
            rec= Reclamo.objects.all().select_related('deudas_reclamos').select_related('prioridad_reclamos')
            # slug=Reclamo.objects.all(slug=self.kwargs['slug'])
            # movs=Movimiento.objects.filter(id_rec=slug).order_by('-fch_std_mov')
            # prior=Rec_Prioridad.objects.get(id_rec=slug)
            
            
            context={
                
                'reclamos':rec,
                
            }
            return  context
        
        
        
        def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
            return redirect('index')

#class AddPrioridad(LoginRequiredMixin, PermissionRequiredMixin ,SuccessMessageMixin,CreateView):
class AddReclamo(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,CreateView):
     model=Reclamo
     template_name='add_reclamo.html'
     form_class=ReclamoForm
     success_url=reverse_lazy('list_reclamos')
     permission_required = "reclamo.add_reclamo"
    
   
    
     def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
         try:
            
             if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    
#                     #recupero datos del formulario
                     form=ReclamoForm(data=request.POST)
                     if form.is_valid():
                         fch_act=timezone.datetime.today()
                         new_clase=form.save(commit=False)
                         new_clase.user_rec=request.user  #este es el user que inicio sesion
                         new_clase.save()
                         instance_std_mov, created_std_mov=EstadoMov.objects.get_or_create(dsc_std_mov='INICIO', defaults={'user_std_mov':request.user})
                         #crear el primer movimiento para registrar la prioridad y la deuda
                         instance_mov=Movimiento.objects.create( fch_mov=fch_act, id_rec=new_clase,id_std_mov=instance_std_mov, gde_mov=request.POST.get("gde_mov", "").upper(), obs_mov='Incorporación Reclamo al R.U.P.', fch_std_mov=fch_act,user_mov=request.user )
                         #crear la prioridad inicial
                         minprior=Prioridad.objects.all().aggregate(Min('nivel_prior'))
                         prior=Prioridad.objects.get(nivel_prior=minprior['nivel_prior__min'])
                         norma_legal_rec=new_norma_prior=request.POST.get('norma_legal_rec',"")
                         prioridad=Rec_Prioridad.objects.create(id_rec=new_clase,id_prior=prior, id_mov=instance_mov, orden=0, user_rec_prior=request.user, norma_legal_prior=norma_legal_rec )
                         deuda= Deuda.objects.create(id_rec=new_clase, user_deuda= request.user, fch_calculo= timezone.datetime.today())
                         
                         
                         orden=Orden()
                         orden.recalc_prior(request.user, timezone.datetime.today())
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
                 return redirect ('list_reclamos')        
                    
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
class EditReclamo(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,UpdateView):        
     model=Reclamo
     template_name='edit_reclamo.html'
     form_class=ReclamoForm
     success_url=reverse_lazy('list_reclamos')
     success_message='Registro editado correctamente'
     permission_required = "reclamo.change_reclamo"
    
     def get_form_kwargs(self):
        print('get_form_kwargs')
        kwargs = super(EditReclamo, self).get_form_kwargs()
        # Remove the post object as instance, 
        # since we are working with a comment
        #kwargs.pop('instance', None)
        kwargs['required'] = False
       
        return kwargs
        
        
     def form_valid(self, form):
             print('form_valid')
             form.instance.user_rec=self.request.user
             form.instance.gde_mov=self.request.user
             return super().form_valid(form)
        
     def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
             #return HttpResponseRedirect(reverse_lazy(self.success_url))
            return JsonResponse({'message': 'Acceso Denegado'}, status=401)

     def post(self, request: HttpRequest,slug, *args: str, **kwargs: Any) -> HttpResponse:
         
         try:
            
             if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    
#                     #recupero datos del formulario
                     verif=Verif_Lotes()
                     
                     form=ReclamoForm(data=request.POST, instance=self.get_object(),required=False)
                     estado=request.POST.get("std_rec", "")
                     
                     if verif.supl_rec(slug, estado):
                         mensaje='No se puede modificar reclamo'
                        
                         error=['Reclamo sin Suplementaria']
                         response=JsonResponse({'mensaje':mensaje, 'error':error})
                         response.status_code=400
                         return response
                     
                     
                     if not verif.deuda_rec(slug, estado):
                         mensaje='No se puede modificar reclamo'
                        
                         error=['Reclamo sin Importe de Deuda']
                         response=JsonResponse({'mensaje':mensaje, 'error':error})
                         response.status_code=400
                         return response
                         
                     
                     if verif.rec_in_lote(slug):
                         mensaje='No se puede modificar reclamo'
                        
                         error=['Reclamo en lote cerrado']
                         response=JsonResponse({'mensaje':mensaje, 'error':error})
                         response.status_code=400
                         return response
                     
                        
                         
                     elif form.is_valid():
                         
                         
                         new_clase=form.save(commit=False)
                         new_clase.user_rec=request.user 
                         if not verif.unico_lote(slug, estado, request.user): 
                             new_clase.save() 
                             calc=Calc_Lotes()
                             calc.rec_lote(request.user,0)
                         else:
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
             print('entro en la exeption***********')
             print(e)
             mensaje='No se ha podido editar el Registro'
             error="e"
             response=JsonResponse({'mensaje':mensaje, 'error':error})
             response.status_code=400
             return response
      
      
# class DeleteMarca(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
class DeleteReclamo(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,DeleteView):
     model=Reclamo
     template_name='del_reclamo.html'  #o crear marca_confirm_delete.html y esta linea se omite
     permission_required = "reclamo.delete_reclamo"
     success_url=reverse_lazy('list_reclamos')
   
 
    
     def post(self, request,slug, *args, **kwargs) -> HttpResponse:
        
        
         try:
             verif=Verif_Lotes()
             if verif.rec_in_lote(slug):
                       messages.add_message(request=request, level=messages.ERROR,message='El Registro No se puede Eliminar se encuentra en lote cerrado')
             
             else:
                clase=Reclamo.objects.get(slug=slug)
                usuario=request.user
             
                hist_clase= HistReclamo.objects.create(
                    id_rec=clase.id_rec,
                    id_legajo=clase.id_legajo,
                    id_tipo_rec=clase.id_tipo_rec,
                    fch_dsd_rec=clase.fch_dsd_rec,
                    fch_hst_rec=clase.fch_hst_rec,
                    dias_rec=clase.dias_rec,
                    norma_legal_rec=clase.norma_legal_rec,
                    resol_pago_rec=clase.resol_pago_rec,
                    nro_supl=clase.nro_supl,
                    year_credito=clase.year_credito,
                    std_rec=clase.std_rec,
                    gde_mov=clase.gde_mov,
                    fch_rec=clase.fch_rec,
                    user_rec=clase.user_rec.username,
                    slug=clase.slug,
                    h_user_proc=usuario,
                    h_tipo_proc='D')
                
                clase.delete()
                messages.add_message(request=request, level=messages.SUCCESS,message='Registro Eliminado Correctamente') 
        
         except:
             messages.add_message(request=request, level=messages.ERROR,message='El Registro No se puede Eliminar') 
                                             
         finally:
             return redirect('list_reclamos')
    
     def handle_no_permission(self):
        messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
         #return HttpResponseRedirect(reverse_lazy(self.success_url))
        return JsonResponse({'message': 'Acceso Denegado'}, status=401)


class EditSuple(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,UpdateView):        
     model=Reclamo
     template_name='edit_supl.html'
     form_class=SuplForm
     success_url=reverse_lazy('list_reclamos')
     success_message='Registro editado correctamente'
     permission_required = "reclamo.change_reclamo"
    
     def get_form_kwargs(self):
        print('get_form_kwargs')
        kwargs = super(EditSuple, self).get_form_kwargs()
        # Remove the post object as instance, 
        # since we are working with a comment
        #kwargs.pop('instance', None)
        #kwargs['required'] = False
       
        return kwargs
        
        
     def form_valid(self, form):
             print('form_valid')
             form.instance.user_rec=self.request.user
            
             return super().form_valid(form)
        
     def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
             #return HttpResponseRedirect(reverse_lazy(self.success_url))
            return JsonResponse({'message': 'Acceso Denegado'}, status=401)

     def post(self, request: HttpRequest,slug, *args: str, **kwargs: Any) -> HttpResponse:
         
         try:
            
             if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    
#                     #recupero datos del formulario
                     verif=Verif_Lotes()
                     
                     form=SuplForm(data=request.POST, instance=self.get_object())
                     if verif.rec_in_lote(slug):
                         mensaje='No se puede modificar reclamo'
                        
                         error=['Reclamo en lote cerrado']
                         response=JsonResponse({'mensaje':mensaje, 'error':error})
                         response.status_code=400
                         return response
                         
                     elif form.is_valid():
                         
                         new_clase=form.save(commit=False)
                         new_clase.user_rec=request.user 
                         
                         new_clase.save()   
                            
                         
                         
                         
                         mensaje='Datos Supl. Editados Correctamente'
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
             print('entro en la exeption***********')
             print(e)
             mensaje='No se ha podido editar el Registro'
             error="e"
             response=JsonResponse({'mensaje':mensaje, 'error':error})
             response.status_code=400
             return response
     

def rec_in_lote(slug):
    rec=Rec_Lote.objects.filter(id_rec__slug=slug, id_lote__activo_lote=False)
    if rec:
        return True
    
    return False
    
    