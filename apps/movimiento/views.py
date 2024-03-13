from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
#------------------------------------------------------------
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from .models import Movimiento, HistMovimiento
from .forms import MovimientoForm
from apps.reclamo.models import Reclamo
from apps.rec_prioridad.models import Rec_Prioridad
from django.contrib.messages.views import SuccessMessageMixin
from apps.lote.verif_reclamo import Verif_Lotes


def home(request,slug):
    
    return render(request, 'index.html', {})
    
#class ListPrioridad(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,ListView): 
class ListMovimientos(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,ListView): 
        model=Movimiento
        template_name='movimientos.html'
        permission_required = "movimiento.view_movimiento"    
        
        
        def get_context_data(self,**kwargs):
            
                try:
                        context = super().get_context_data(**kwargs)
                        slug=Reclamo.objects.get(slug=self.kwargs['slug'])
                        movs=Movimiento.objects.filter(id_rec=slug).order_by('-fch_std_mov')
                        prior=Rec_Prioridad.objects.get(id_rec=slug)
                        context={
                            'detalles':movs,
                            'reclamo':slug,
                            'slug_prior':prior.slug
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
class AddMovimiento(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,CreateView):
     model=Movimiento
     template_name='add_mov_rec.html'
     form_class=MovimientoForm
     #success_url=reverse_lazy('list_tipos_rec')
     permission_required = "movimiento.add_movimiento"
    
     def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        rec = Reclamo.objects.get(slug=self.kwargs['slug'])
        #paso los parametros recibidos en el get, mas los datos del reclamo y los envio a form.modelForm
        #para generar el formulario
        kwargs.update({ 'slug':self.kwargs['slug']})
        
       
        return kwargs
    
     def get_context_data(self, **kwargs):
         
            try:
                context = super().get_context_data(**kwargs)
                slug = self.kwargs.get('slug')
                rec = Reclamo.objects.get(slug=self.kwargs['slug'])
                context['slug'] = slug
                context['reclamo'] = rec
                return context
            
            
            except Exception as e:
                print('entro en la exeption***********')
                print(e)
                mensaje='No se ha podido editar el Registro'
                error="e"
                response=JsonResponse({'mensaje':mensaje, 'error':error})
                response.status_code=400
                return response
    
     def form_valid(self, form):
              
              form.instance.user_mov=self.request.user
              return super().form_valid(form)
     
     def post(self, request: HttpRequest, slug, *args: str, **kwargs: Any) -> HttpResponse:
         
         
         try:
            
             if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                     reclamo=Reclamo.objects.get(slug=slug)  
                     
                                        
#                     #recupero datos del formulario
                     form=MovimientoForm(data=request.POST, initial={'id_rec':reclamo})
                     form = MovimientoForm(request.POST)
                    
                    
                     if form.is_valid():
                       
                         new_clase=form.save(commit=False)
                         new_clase.user_mov=request.user  #este es el user que inicio sesion
                         new_clase.id_rec=reclamo
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
                 return redirect ('list_detalles')        
                    
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
        

 
class EditMovRec(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,UpdateView):        
     model=Movimiento
     template_name='edit_mov_rec.html'
     form_class=MovimientoForm
     success_url=reverse_lazy('list_detalles')
     success_message='Registro editado correctamente'
     permission_required = "movimiento.change_movimiento"
    
     
    
    
     def form_valid(self, form):
             form.instance.user_mov=self.request.user
             return super().form_valid(form)
        
     def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
             #return HttpResponseRedirect(reverse_lazy(self.success_url))
            return JsonResponse({'message': 'Acceso Denegado'}, status=401)

     def post(self, request: HttpRequest,slug, *args: str, **kwargs: Any) -> HttpResponse:
        
         try:
            
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                     mov=Movimiento.objects.get(slug=slug)
                     
                     reclamo=Reclamo.objects.get(slug=mov.id_rec.slug)
                     
                     slug_rec=reclamo.slug 
                     
                     
                     
                                        
#                     #recupero datos del formulario

                     form=MovimientoForm(data=request.POST, instance=self.get_object(),initial={'id_rec':reclamo})
                     #form = MovimientoForm(request.POST)
                     verif=Verif_Lotes()
                     
                     
                     if verif.rec_in_lote(reclamo.slug):
                         mensaje='No se puede modificar reclamo'
                        
                         error=['Reclamo en lote cerrado']
                         response=JsonResponse({'mensaje':mensaje, 'error':error})
                         response.status_code=400
                         return response
                    
                     elif form.is_valid():
                       
                         new_clase=form.save(commit=False)
                         new_clase.user_mov=request.user  #este es el user que inicio sesion
                         new_clase.id_rec=reclamo
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
               
                 return redirect ('list_detalles' , slug_rec) 
            
            
            

         except Exception as e:
             print('entro en la exeption***********')
             print(e)
             mensaje='No se ha podido editar el Registro'
             error="e"
             response=JsonResponse({'mensaje':mensaje, 'error':error})
             response.status_code=400
             return response
      
      
# class DeleteMarca(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
class DeleteMovRec(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin,DeleteView):
     model=Movimiento
     template_name='del_mov_rec.html'  #o crear marca_confirm_delete.html y esta linea se omite
     permission_required = "movimiento.delete_movimiento"
     success_url=reverse_lazy('list_detalles')
   
    #  def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     rec_slug = self.kwargs.get('rec_slug')
    #     rec = Reclamo.objects.get(slug=self.kwargs['slug'])
        
    #     context['rec_slug'] = rec_slug
    #     context['reclamo'] = rec
    #     return context
    
     def post(self, request,slug, *args, **kwargs) -> HttpResponse:
         try:
             
             verif=Verif_Lotes()
             clase=Movimiento.objects.get(slug=slug)
             
             
             if verif.rec_in_lote(clase.id_rec.slug):
                
                messages.add_message(request=request, level=messages.ERROR,message='El Registro No se puede Eliminar se encuentra en lote cerrado')
             
             else:
               
                usuario=request.user
             
                hist_clase= HistMovimiento.objects.create(
                 id_mov=clase.id_mov,
                 fch_mov=clase.fch_mov,
                 id_rec=clase.id_rec,
                 id_std_mov=clase.id_std_mov.dsc_std_mov,
                 gde_mov=clase.gde_mov,
                 obs_mov=clase.obs_mov,
                 fch_std_mov=clase.fch_std_mov,
                 fch_mov_user=clase.fch_mov_user,
                 user_mov=clase.user_mov.username,
                 slug=clase.slug,
                 h_user_proc=usuario,
                 h_tipo_proc='D')
                
                clase.delete()
                messages.add_message(request=request, level=messages.SUCCESS,message='Registro Eliminado Correctamente') 
             
             
                  
         except:
             messages.add_message(request=request, level=messages.ERROR,message='El Registro No se puede Eliminar') 
                                             
         finally:
             return redirect('list_detalles', clase.id_rec.slug)
    
     def handle_no_permission(self):
        messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
         #return HttpResponseRedirect(reverse_lazy(self.success_url))
        return JsonResponse({'message': 'Acceso Denegado'}, status=401)