from typing import Any, Dict
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
#------------------------------------------------------------
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from .models import MovData
from .forms import MovDataForm, RecuperarForm, TransferirForm, AdquirirForm
from django.contrib.messages.views import SuccessMessageMixin
from apps.estado.models import Estado
from apps.oficina.models import Oficina
from django.db.models import Q,F
from apps.operador.models import Operador
import sys
from django.db import transaction
from apps.bien.models import Bien
from apps.bien.forms import InventariarForm



    
class ListMovData(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,ListView): 
        model=MovData 
        template_name='movdatas.html'
        permission_required = "movdata.view_movdata"
        
         
        
        def get_queryset(self):
            # original qs
            qs = super().get_queryset() 
            # filter by a variable captured from url, for example
            #return qs.filter(name__startswith=self.kwargs['name'])
            return qs.filter(id_mov=0)
            
        
        def get_context_data(self,**kwargs):
            
            try:
                    context = super(ListMovData, self).get_context_data(**kwargs)
                    oficina=Operador.objects.get(operador=self.request.user)
                    result=[]
                    result=oficinas_user(oficina.oficina_id, result)
                    
                    
                    origen=MovData.objects.filter(fch_hst=None,bien_mov__no_inventariado=False,origen_id__in=result, destino_id__in=result)

                    deotros=MovData.objects.filter(~Q(origen_id__in=result) & Q(fch_hst=None) & Q(destino_id__in=result))

                    prestados=MovData.objects.filter(Q(origen_id__in=result) & Q(fch_hst=None) & ~Q(destino_id__in=result))
                    
                    noinventariados=MovData.objects.filter(fch_hst=None,bien_mov__no_inventariado=True,origen_id__in=result, destino_id__in=result)
                    
                    context['origen'] = origen
                    context['destino'] = deotros
                    context['origenes'] = prestados
                    context['sininventario'] = noinventariados
                    
                    return context
            except:
                    messages.add_message(request=self.request, level=messages.ERROR,message='Operador sin destino') 
                    return None
    
        def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
            return redirect('index')
    
class AddMovData(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin, CreateView):
    model=MovData
    template_name='add_movdata.html'
    form_class=MovDataForm
    permission_required = "movdata.add_movdata"
    success_url=reverse_lazy('list_movdatas')
    
    def form_valid(self, form):
        if form.save(self):
            return super(AddMovData, self).form_valid(form)
        else:
            return self
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
            
            try:
                form=MovDataForm(request.POST)
                new_clase=form.save(commit=False) 
                new_clase.user_mov=request.user
                estado=Estado.objects.get(pk=(request.POST['estado'] ))
                if  not estado.origen:            
                    new_clase.origen_id=request.POST['destino']   
                    mov=MovData.objects.filter(bien_mov_id=(request.POST['bien_mov']),fch_hst=None).update(fch_hst=timezone.now())
                    
                else:
                    mov= MovData.objects.select_for_update().filter(bien_mov_id=(request.POST['bien_mov']),fch_hst=None).first()
                    if mov:
                        mov.fch_hst=timezone.now()
                        mov.save()
                        cod_origen=(mov.origen_id)
                        new_clase.origen_id=cod_origen
                    else:
                        new_clase.origen_id=request.POST['destino']
                    
                
                
                
                new_clase.save()
                messages.add_message(request=request, level=messages.SUCCESS,message='Registro Creado Correctamente') 
                return redirect ('list_movdatas')
            except:
                messages.add_message(request=request, level=messages.ERROR,message='Error Registro') 
                return redirect ('list_movdatas')
      
    def handle_no_permission(self):
        messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
         #return HttpResponseRedirect(reverse_lazy(self.success_url))
        return JsonResponse({'message': 'Acceso Denegado'}, status=401)  
        
class EditMovData( LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
    model=MovData
    template_name='edit_movdata.html'
    form_class=MovDataForm
    success_url=reverse_lazy('list_movdatas')
    success_message='Registro editado correctamente'
    permission_required = "movdata.change_movdata"
    
    
    def form_valid(self, form):
            form.instance.user_mov=self.request.user
            return super().form_valid(form)

    def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
             #return HttpResponseRedirect(reverse_lazy(self.success_url))
            return JsonResponse({'message': 'Acceso Denegado'}, status=401)
        
class DeleteMovData(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,DeleteView):
    model=MovData
    template_name='del_movdata.html'  #o crear marca_confirm_delete.html y esta linea se omite
    permission_required = "movdata.delete_movdata"
    success_url=reverse_lazy('list_movdatas')
    
    def post(self, request,slug, *args, **kwargs) -> HttpResponse:
        try:
            marca=MovData.objects.get(slug=slug)
            marca.delete()
            messages.add_message(request=request, level=messages.SUCCESS,message='Registro Eliminado Correctamente') 
        
        except:
            messages.add_message(request=request, level=messages.ERROR,message='El Registro No se puede Eliminar') 
        
        finally:
            return redirect('list_movdatas')
    
    def handle_no_permission(self):
        messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
        return JsonResponse({'message': 'Acceso Denegado'}, status=401)
    
    


class Recuperar(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,View):
    
    permission_required = "movdata.view_movdata"
    success_url=reverse_lazy('list_movdatas')
    
    def get(self, request,slug, *args, **kwargs):
        #data=MovData.objects.get(slug=slug)
        form=RecuperarForm()
        
        params = {
            'form':form,
            'slug':slug,
        }     
        return render(request, 'recuperar.html',params)
    
    def post(self, request,slug, *args, **kwargs):
        
        data_mov=MovData.objects.get(slug=slug)
        origen_mov=data_mov.origen
        bien=data_mov.bien_mov
        instance_est, created_std=Estado.objects.get_or_create(dsc_estado='ACTIVO', defaults={'user_estado':request.user,'origen':False})
        gde= request.POST['gde_mov'],
        obs= request.POST['observ_mov'],
        user= request.user
        new_mov=MovData(bien_mov=bien, origen=origen_mov, destino=origen_mov, estado=instance_est,gde_mov=gde, observ_mov=obs, user_mov=user)
        data_mov.fch_hst=timezone.now()
        with transaction.atomic():
                new_mov.save()
                data_mov.save()
        
        return redirect ('list_movdatas')
       
    def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
            return JsonResponse({'message': 'Acceso Denegado'}, status=401)

class Adquirir(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,View):
    permission_required = "movdata.view_movdata"
    
    success_url=reverse_lazy('list_movdatas')
    
    def get(self, request,slug, *args, **kwargs):
       
        params = {
            'form': AdquirirForm,
            'slug':slug,
        }
       
        return render(request, 'adquirir.html',params)
    
    
    def post(self, request,slug, *args, **kwargs):
        
        data_mov=MovData.objects.get(slug=slug)
        origen_mov=data_mov.destino
        bien=data_mov.bien_mov
        instance_est, created_std=Estado.objects.get_or_create(dsc_estado='ACTIVO', defaults={'user_estado':request.user,'origen':False})
        gde= request.POST['gde_mov'],
        obs= request.POST['observ_mov'],
        user= request.user
        new_mov=MovData(bien_mov=bien, origen=origen_mov, destino=origen_mov, estado=instance_est,gde_mov=gde, observ_mov=obs, user_mov=user)
        data_mov.fch_hst=timezone.now()
        with transaction.atomic():
                new_mov.save()
                data_mov.save()
        
        return redirect ('list_movdatas')
 
    def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
            return JsonResponse({'message': 'Acceso Denegado'}, status=401)
                      
class Inventariar(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
    
    model=Bien
    template_name='inventariar.html'
    form_class=InventariarForm
    success_url=reverse_lazy('list_movdatas')
    success_message='Registro editado correctamente'
    permission_required = "movdata.view_movdata"
    
    
    def form_valid(self, form):
          
            form.instance.user_bien=self.request.user
            return super().form_valid(form)
        
    
    def handle_no_permission(self):
        messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
        return JsonResponse({'message': 'Acceso Denegado'}, status=401)
                 
class Transferir(LoginRequiredMixin, CreateView):
    model=MovData
    template_name='transferir.html'
    form_class=TransferirForm
    permission_required = "movdata.view_movdata"
    success_url=reverse_lazy('list_movdatas')
        
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        result=[]
        oficina=Operador.objects.get(operador=self.request.user)
        result=oficinas_user(oficina.oficina_id, result)
        ofi_user=Oficina.objects.filter(id_oficina__in=result)
        
        #paso los parametros recibidos en el get, mas los datos de oficina y los envio a form.modelForm
        #para generar el formulario
        kwargs.update({'request': self.request, 'result':ofi_user, 'slug':self.kwargs['slug']})
        return kwargs
    
    """def get_context_data(self, **kwargs):
        print(self.kwargs['slug'])
        context = super(Transferir, self).get_context_data(**kwargs)
        context = {
            'slug':  self.kwargs['slug'],
            'form': self.form_class
        }
        return context"""
     
    def post(self, request: HttpRequest, slug, *args: str, **kwargs: Any) -> HttpResponse:
            
            try:
                bien_trans= Bien.objects.get(slug=slug)
                
                form=MovDataForm(request.POST)
                
                if form.is_valid():
                    
                    new_clase=form.save(commit=False) 
                    new_clase.user_mov=request.user
                    new_clase.bien_mov=bien_trans
                    estado=Estado.objects.get(pk=(request.POST['estado'] ))
                    if  not estado.origen:            
                        new_clase.origen_id=request.POST['destino']   
                        mov=MovData.objects.filter(bien_mov_id=bien_trans,fch_hst=None).update(fch_hst=timezone.now())
                    
                    else:
                        mov= MovData.objects.select_for_update().filter(bien_mov_id=bien_trans,fch_hst=None).first()
                        if mov:
                            mov.fch_hst=timezone.now()
                            mov.save()
                            cod_origen=(mov.origen_id)
                            new_clase.origen_id=cod_origen
                        else:
                            new_clase.origen_id=request.POST['destino']
                    
                
                
                
                    new_clase.save()
                    messages.add_message(request=request, level=messages.SUCCESS,message='Registro Creado Correctamente') 
                    return redirect ('list_movdatas')
                else:
                    messages.add_message(request=request, level=messages.Error,message='Error en Registro') 
                    return redirect ('transferir')
            except:
                messages.add_message(request=request, level=messages.ERROR,message='Error Registro') 
                return redirect ('list_movdatas')

    def handle_no_permission(self):
            messages.add_message(request=self.request, level=messages.ERROR,message='Acceso Denegado') 
            return JsonResponse({'message': 'Acceso Denegado'}, status=401)

def oficinas_user(id_oficina,result):
    
    result.append(id_oficina)
    oficina = Oficina.objects.filter(id_oficina_padre=id_oficina)
    if oficina:
        for of in oficina:
            result = oficinas_user(of.id_oficina, result)
    return result


