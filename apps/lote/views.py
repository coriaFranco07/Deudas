from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
#------------------------------------------------------------
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from .models import Lote, HistLote
from .forms import LoteForm
from django.contrib.messages.views import SuccessMessageMixin
from .lotes import Calc_Lotes
from .pago import Pago_Lote
from django.contrib.auth.decorators import login_required, permission_required
from apps.rec_lote.models import Rec_Lote
from django.db.models import Sum,Count, Max, Min


    
#class ListPrioridad(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,ListView): 
class Listlote(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,ListView): 
        model=Lote
        template_name='lotes.html'
        context_object_name='lotes' 
        queryset = Lote.objects.filter(activo_lote=False)
        permission_required = "lote.view_lote"
        
        def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
            return redirect('index')
    
    
class ListloteAcivo(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,ListView): 
        model=Lote
        template_name='lotes_act.html'
        context_object_name='lotes' 
        queryset = Lote.objects.filter(activo_lote=True)
        permission_required = "lote.view_lote"
        
        def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
            return redirect('index')
        

class AddLote(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,CreateView):
     model=Lote
     template_name='add_lote.html'
     form_class=LoteForm
     success_url=reverse_lazy('list_lotes_a')
     permission_required = "lote.add_lote"
    
   
    
     def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
         try:
            
             if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    
#                     #recupero datos del formulario
                     form=LoteForm(data=request.POST)
                     if form.is_valid():
                       
                         new_clase=form.save(commit=False)
                         new_clase.user_lote=request.user  #este es el user que inicio sesion
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
                 return redirect ('list_lotes')        
                    
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
        

#class EditLote(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
class EditLote(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,UpdateView):        
     model=Lote
     template_name='edit_lote.html'
     form_class=LoteForm
     success_url=reverse_lazy('list_lotes_a')
     success_message='Registro editado correctamente'
     permission_required = "lote.change_lote"
    
    
     def form_valid(self, form):
             form.instance.user_lote=self.request.user
             return super().form_valid(form)
        
     def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
             #return HttpResponseRedirect(reverse_lazy(self.success_url))
            return JsonResponse({'message': 'Acceso Denegado'}, status=401)

     def post(self, request: HttpRequest,slug, *args: str, **kwargs: Any) -> HttpResponse:
        
         try:
            
             if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                 
                     loteinrec = Rec_Lote.objects.filter(id_lote__slug=slug).aggregate(suma=Sum('id_rec__deudas_reclamos__total'))
                     
                     total=float(request.POST.get('importe_lote'))
                     gastos=float(loteinrec['suma'])
                     
                     
                     saldo=total-gastos
#                     #recupero datos del formulario
                     form=LoteForm(data=request.POST, instance=self.get_object())
            
                     if form.is_valid():
                         new_clase=form.save(commit=False)
                         new_clase.user_lote=request.user 
                         new_clase.saldo_lote= saldo
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
               
                 return redirect ('list_lotes_a') 
            
            
            

         except Exception as e:
             
             mensaje='No se ha podido editar el Registro'
             error="e"
             response=JsonResponse({'mensaje':mensaje, 'error':error})
             response.status_code=400
             return response
      
      

class DeleteLote(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
     model=Lote
     template_name='del_lote.html'  #o crear marca_confirm_delete.html y esta linea se omite
     permission_required = "lote.delete_lote"
     success_url=reverse_lazy('list_lotes')
   
 
    
     def post(self, request,slug, *args, **kwargs) -> HttpResponse:
         try:
             clase=Lote.objects.get(slug=slug)
             usuario=request.user
             
             hist_clase= HistLote.objects.create(
                 id_lote=clase.id_lote,
                 nivel_lote=clase.nivel_lote,
                 year_lote=clase.year_lote,
                 activo_lote=clase.activo_lote,
                 importe_lote=clase.importe_lote,
                 saldo_lote=clase.saldo_lote,
                 fch_lote=clase.fch_lote,
                 user_lote=clase.user_lote.username,
                 slug=clase.slug,
                 h_user_proc=usuario,
                 h_tipo_proc='D')
             
             
             clase.delete()
             messages.add_message(request=request, level=messages.SUCCESS,message='Registro Eliminado Correctamente') 
        
         except:
             messages.add_message(request=request, level=messages.ERROR,message='El Registro No se puede Eliminar') 
        
         finally:
             return redirect('list_lotes')
    
     def handle_no_permission(self):
        messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
         #return HttpResponseRedirect(reverse_lazy(self.success_url))
        return JsonResponse({'message': 'Acceso Denegado'}, status=401)


@login_required
@permission_required("lote.delete_lote")
def calcular_lotes(request,user, val):
    
    lote_calc=Calc_Lotes()
    lote_calc.rec_lote(user, val)
    
    return redirect('list_lotes_a')

@login_required
@permission_required("lote.delete_lote")
def pagar_lote(request, slug ,user):
    
    
    lote_calc=Pago_Lote()
    saldo=Lote.objects.get(slug=slug)
    loteinrec = Rec_Lote.objects.filter(id_lote__slug=slug).aggregate(suma=Sum('id_rec__deudas_reclamos__total'))
    if saldo.importe_lote != float(loteinrec['suma']):
       messages.add_message(request=request, level=messages.ERROR,message=f'Deuda de Reclamos no se Ajustan al importe del Lote ${saldo.importe_lote} ')      
    
    elif saldo.saldo_lote>0:
       
        messages.add_message(request=request, level=messages.ERROR,message=f'Verifique Saldo del lote, sobran ${saldo.saldo_lote} ') 
    
    
    
    elif not lote_calc.pagar_lote(slug, user):
          print('dos')  
          messages.add_message(request=request, level=messages.ERROR,message='Invalido, Reclamos sin Suplementarias en el Lote') 
    
    else:
        print('tres')
        messages.add_message(request=request, level=messages.SUCCESS,message='Lote Pagado Correctamente') 
    
    return redirect('list_lotes_a')