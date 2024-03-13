from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from  apps.deuda.models import Deuda
from datetime import datetime, date
from django.db.models import Sum,Count, Max, Min
from apps.reclamo.models import Reclamo
from apps.tipo_reclamo.models import TipoReclamo
from apps.movimiento.models import Movimiento
from apps.lote.models import Lote
from django.http import JsonResponse
from django.template.loader import get_template
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, View
from apps.rec_lote.models import Rec_Lote
from apps.std_mov.models import EstadoMov
from apps.estado.models import Estado
from django.core import serializers
from functools import reduce
from django.db.models import Prefetch
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required, permission_required
 
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

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def total_rec_pagados(request):
   
   try:
            total = Deuda.objects.filter(id_rec__std_rec__dsc_std='RECLAMO PAGADO').aggregate(Sum('total'))['total__sum']
        
            if request.method == "GET":
                
                return JsonResponse({'total': total})
   except Exception as e:
             print('entro en la exeption***********')
             print(e)
             mensaje='No se ha podido editar el Registro'
             error="e"
             response=JsonResponse({'mensaje':mensaje, 'error':error})
             response.status_code=400
             return response


class TiposRecView(LoginRequiredMixin,SuccessMessageMixin,JSONResponseMixin, View):
  template_name = 'home.html'
  output_template = get_template('home.html')

  def get(self, request, *args, **kwargs):
      
        try: 
    #obj = self.get_object()
            tipos = TipoReclamo.objects.all()
            
            label = []
            data = []
            for tip in tipos:
                deuda = Deuda.objects.filter(id_rec__id_tipo_rec__dsc_tipo_rec=tip.dsc_tipo_rec).aggregate(Sum('total'))
                if not deuda['total__sum']:
                    deuda['total__sum'] = 0
                label.append(tip.dsc_tipo_rec)
                data.append(deuda['total__sum'])

            x = list(zip(label, data))

            x.sort(key=lambda x: x[1], reverse=True)
            x = list(zip(*x))
            
            #return JsonResponse({'labels': x[0][:3], 'data': x[1][:3]})
            
            return self.render_to_json_response({'labels': x[0][:3], 'data': x[1][:3]})

        except Exception as e:
             print('entro en la exeption***********')
             print(e)
             mensaje='No se ha podido editar el Registro'
             error="e"
             response=JsonResponse({'mensaje':mensaje, 'error':error})
             response.status_code=400
             return response

class RecPeriodosView(LoginRequiredMixin,SuccessMessageMixin,JSONResponseMixin, View):
    template_name = 'home.html'
    output_template = get_template('home.html')

    def get(self, request, *args, **kwargs):
        
        
        try:
                x =Deuda.objects.all()
                movs=EstadoMov.objects.all().order_by('dsc_std_mov')
            
                meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Set', 'Oct', 'Nov', 'Dic']
                data = []
                labels = []
                mo=[]
                cont = 0
                mes = datetime.now().month + 1
                ano = datetime.now().year
                for i in range(12): 
                    mes -= 1
                    if mes == 0:
                        mes = 12
                        ano -= 1
                    
                    y = sum([i.total for i in x if i.id_rec.fch_dsd_rec.month == mes and i.id_rec.fch_dsd_rec.year == ano])
                    labels.append(meses[mes-1])
                    data.append(y)
                    cont += 1

                    
                #movi=serializers.serialize('json', movs)
                # print(movi)
                for mos in movs:
                    
                    movim={
                        'id_std_mov':mos.id_std_mov,
                        'dsc_std_mov': mos.dsc_std_mov,
                    }
                    mo.append(movim)
       
                
                return self.render_to_json_response({'data': data[::-1], 'labels': labels[::-1], 'movs':mo})
            
        except Exception as e:
             print('entro en la exeption***********')
             print(e)
             mensaje='No se ha podido editar el Registro'
             error="e"
             response=JsonResponse({'mensaje':mensaje, 'error':error})
             response.status_code=400
             return response    
            
        
class RecPedienteView(LoginRequiredMixin,SuccessMessageMixin,JSONResponseMixin, View):
    template_name = 'home.html'
    output_template = get_template('home.html')

    def get(self, request, *args, **kwargs):
        
        try:
                
                total = Deuda.objects.filter(id_rec__std_rec__act_calculo=True, total__gt=0).aggregate(Sum('total'))['total__sum']
                    
                return self.render_to_json_response({'total': total})
        except Exception as e:
             print('entro en la exeption***********')
             print(e)
             mensaje='No se ha podido editar el Registro'
             error="e"
             response=JsonResponse({'mensaje':mensaje, 'error':error})
             response.status_code=400
             return response
        
class RecPagadoView(LoginRequiredMixin,SuccessMessageMixin,JSONResponseMixin, View):
    template_name = 'home.html'
    output_template = get_template('home.html')

    def get(self, request, *args, **kwargs):
        
        try:
                
                total = Deuda.objects.filter(id_rec__std_rec__dsc_std='RECLAMO PAGADO').aggregate(Sum('total'))['total__sum']
                    
                return self.render_to_json_response({'total': total})
            
        except Exception as e:
             print('entro en la exeption***********')
             print(e)
             mensaje='No se ha podido editar el Registro'
             error="e"
             response=JsonResponse({'mensaje':mensaje, 'error':error})
             response.status_code=400
             return response
     
class PresupuestoView(LoginRequiredMixin,SuccessMessageMixin,JSONResponseMixin, View):
    template_name = 'home.html'
    output_template = get_template('home.html')

    def get(self, request, *args, **kwargs):
        
        try:
                
                total = Lote.objects.filter(activo_lote=True).aggregate(Sum('importe_lote'))['importe_lote__sum']
            
                return self.render_to_json_response({'total': total})
 
        except Exception as e:
             print('entro en la exeption***********')
             print(e)
             mensaje='No se ha podido editar el Registro'
             error="e"
             response=JsonResponse({'mensaje':mensaje, 'error':error})
             response.status_code=400
             return response

 
 
class RecLoteiew(LoginRequiredMixin,SuccessMessageMixin,JSONResponseMixin, View):
    template_name = 'home.html'
    output_template = get_template('home.html')

    def get(self, request, *args, **kwargs):
        
            try:    
            
                label = []
                data = []  
                
                total = Rec_Lote.objects.all().values('id_lote').annotate(tot=Count('id_rec')).order_by('id_lote')
                
            
                for to in total:
                
                    
                    label.append(to['id_lote'])
                    data.append(to['tot'])

                x = list(zip(label, data))

                x.sort(key=lambda x: x[1], reverse=True)
                x = list(zip(*x))
                    
                
                
            
                return self.render_to_json_response({'data': data[::], 'labels': label[::]})
            
            except Exception as e:
             print('entro en la exeption***********')
             print(e)
             mensaje='No se ha podido editar el Registro'
             error="e"
             response=JsonResponse({'mensaje':mensaje, 'error':error})
             response.status_code=400
             return response
    
class CantTipoRecView(LoginRequiredMixin,SuccessMessageMixin,JSONResponseMixin, View):
  template_name = 'home.html'
  output_template = get_template('home.html')

  def get(self, request, *args, **kwargs):
      
        try:
            
            #obj = self.get_object()
            tipos = Reclamo.objects.all().values('id_tipo_rec__dsc_tipo_rec').annotate(cant=Count('id_tipo_rec')).order_by('id_tipo_rec')
            label = []
            data = []
            for to in tipos:
                
                label.append(to['id_tipo_rec__dsc_tipo_rec'])
                data.append(to['cant'])

            x = list(zip(label, data))

            x.sort(key=lambda x: x[1], reverse=True)
            x = list(zip(*x))
            
            #return JsonResponse({'labels': x[0][:3], 'data': x[1][:3]})
            
            return self.render_to_json_response({'labels': x[0][:3], 'data': x[1][:3]})

        except Exception as e:
             print('entro en la exeption***********')
             print(e)
             mensaje='No se ha podido editar el Registro'
             error="e"
             response=JsonResponse({'mensaje':mensaje, 'error':error})
             response.status_code=400
             return response
    
class TipoMovView(LoginRequiredMixin,SuccessMessageMixin,JSONResponseMixin, View):
  template_name = 'home.html'
  output_template = get_template('home.html')

  def get(self, request, *args, **kwargs):
      
    try:  
            
            #obj = self.get_object()
            tipos = Movimiento.objects.all().values('id_std_mov__dsc_std_mov').annotate(cant=Count('id_rec',distinct=True)).order_by('id_std_mov__dsc_std_mov')
            label = []
            data = []
            for to in tipos:
                
                label.append(to['id_std_mov__dsc_std_mov'])
                data.append(to['cant'])

            x = list(zip(label, data))

            x.sort(key=lambda x: x[1], reverse=True)
            x = list(zip(*x))
            
            #return JsonResponse({'labels': x[0][:3], 'data': x[1][:3]})
            
            return self.render_to_json_response({'labels': x[0][:3], 'data': x[1][:3]})
    except Exception as e:
             print('entro en la exeption***********')
             print(e)
             mensaje='No se ha podido editar el Registro'
             error="e"
             response=JsonResponse({'mensaje':mensaje, 'error':error})
             response.status_code=400
             return response

@login_required
def filtros(request):
    
    return render(request, 'home.html')



    
class FiltroTipoMovView(LoginRequiredMixin,SuccessMessageMixin,JSONResponseMixin, View):
  template_name = 'home.html'
  output_template = get_template('home.html')

  def get(self, request, *args, **kwargs):
    
        try:
    
                filtros=(request.GET.get('param',None))
                
                
                filt=[int(valor) for valor in filtros.split(',')if valor]
            
                
                
                
                
                # rec=Reclamo.objects.prefetch_related(
                #     Prefetch('movs_reclamos', queryset=Movimiento.objects.filter(id_std_mov__dsc_std__constains=dsc))).filter(
                #         std_rec__act_calculo=True)
                
                # print('reclamos----------rec')
                # print(rec)
                
                tipos = Movimiento.objects.filter(id_std_mov__in=filt, id_rec__std_rec__act_calculo=True).values('id_std_mov__dsc_std_mov','id_rec').annotate(cant=Count('id_rec',distinct=True)).order_by('id_std_mov__dsc_std_mov')
                #tiposfilt = Movimiento.objects.filter(reduce(operator.and_, [Q(id_std_mov=c) for c in filt])).filter(id_rec__std_rec__act_calculo=True).values('id_std_mov__dsc_std_mov').annotate(cant=Count('id_rec',distinct=True)).order_by('id_std_mov__dsc_std_mov')
                #tiposfilt = Movimiento.objects.filter(Q(id_std_mov__in=filt, _connector=Q.AND) and (Q(id_rec__std_rec__act_calculo=True))).values('id_rec').annotate(cant=Count('id_rec',distinct=True))
                #print('nuevo lista')
                #print(filt)
                #print('nuevo resultado')
                #print(tiposfilt)
                
                #tip=Movimiento.objects.filter(reduce(operator.and_,(Q(id_std_mov__id_std_mov=id) for id in filt)))
                
                
            
                cont=0
                recla=set()
                rec=[]
                label = []
                data = []
                for to in tipos:
                    recla.add(to['id_rec'])
                    
                for to in tipos:
                    
                    label.append(to['id_std_mov__dsc_std_mov'])
                    data.append(to['cant'])
                    rec.append(to['id_rec'])
                    
            
                for r in recla:
                    if rec.count(r)==len(filt):
                        cont +=1
                    
                
                
                x = list(zip(label, data))
                
                x.sort(key=lambda x: x[1], reverse=True)
                x = list(zip(*x))
            
                #return JsonResponse({'labels': x[0][:3], 'data': x[1][:3]})
                #el label y el data no los ocupo
            
                return self.render_to_json_response({'labels': x[0][:], 'data': x[1][:], 'cant':[cont]})
                
    
        except Exception as e:
             print('entro en la exeption***********')
             print(e)
             mensaje='No se ha podido editar el Registro'
             error="e"
             response=JsonResponse({'mensaje':mensaje, 'error':error})
             response.status_code=400
             return response
   

class FiltrosMovView(LoginRequiredMixin,SuccessMessageMixin,JSONResponseMixin, View):
    template_name = 'home.html'
    output_template = get_template('home.html')

    def get(self, request, *args, **kwargs):
        
            try:         
                
                    movs=EstadoMov.objects.all().order_by('dsc_std_mov')
                    mo=[]
                    
                    for mos in movs:
                        
                        movim={
                            'id_std_mov':mos.id_std_mov,
                            'dsc_std_mov': mos.dsc_std_mov,
                        }
                        mo.append(movim)
                
                            
                    return self.render_to_json_response({'movs':mo})
                
            except Exception as e:
             print('entro en la exeption***********')
             print(e)
             mensaje='No se ha podido editar el Registro'
             error="e"
             response=JsonResponse({'mensaje':mensaje, 'error':error})
             response.status_code=400
             return response    
                    
    
class TiposRecViewTres(LoginRequiredMixin,SuccessMessageMixin,JSONResponseMixin, View):
  template_name = 'home.html'
  output_template = get_template('home.html')

  def get(self, request, *args, **kwargs):
      
        try:
                
                #obj = self.get_object()
                tipos = TipoReclamo.objects.all()
                cant=[]
                label = []
                data = []
                for tip in tipos:
                    deuda = Deuda.objects.filter(id_rec__id_tipo_rec__dsc_tipo_rec=tip.dsc_tipo_rec).aggregate(Sum('total'), Count('id_deuda'))
                    if not deuda['total__sum']:
                        deuda['total__sum'] = 0
                    label.append(tip.dsc_tipo_rec)
                    data.append(deuda['total__sum'])
                    cant.append(deuda['id_deuda__count'])
                
                

                x = list(zip(label, data, cant))
                
                
                
                x.sort(key=lambda x: x[1], reverse=True)
                x = list(zip(*x))
                
            
                
                #return JsonResponse({'labels': x[0][:3], 'data': x[1][:3]})
                
                return self.render_to_json_response({'labels': x[0][:], 'data': x[1][:], 'Cant': x[2][:]})
            
        except Exception as e:
             print('entro en la exeption***********')
             print(e)
             mensaje='No se ha podido editar el Registro'
             error="e"
             response=JsonResponse({'mensaje':mensaje, 'error':error})
             response.status_code=400
             return response


class ReclamosPendView(LoginRequiredMixin,SuccessMessageMixin,JSONResponseMixin, View):
  template_name = 'home.html'
  output_template = get_template('home.html')

  def get(self, request, *args, **kwargs):
      
        try:         
                #obj = self.get_object()
                tipos = TipoReclamo.objects.all()
                cant=[]
                label = []
                data = []
                for tip in tipos:
                    deuda = Deuda.objects.filter(id_rec__id_tipo_rec__dsc_tipo_rec=tip.dsc_tipo_rec, id_rec__std_rec__act_calculo=True).aggregate(Sum('total'), Count('id_deuda'))
                    if not deuda['total__sum']:
                        deuda['total__sum'] = 0
                    label.append(tip.dsc_tipo_rec)
                    data.append(deuda['total__sum'])
                    cant.append(deuda['id_deuda__count'])
                
                

                x = list(zip(label, data, cant))
                
                
                
                x.sort(key=lambda x: x[1], reverse=True)
                x = list(zip(*x))
                
            
                
                #return JsonResponse({'labels': x[0][:3], 'data': x[1][:3]})
                
                return self.render_to_json_response({'labels': x[0][:], 'data': x[1][:], 'Cant': x[2][:]})
            
        except Exception as e:
             print('entro en la exeption***********')
             print(e)
             mensaje='No se ha podido editar el Registro'
             error="e"
             response=JsonResponse({'mensaje':mensaje, 'error':error})
             response.status_code=400
             return response

class CantTipoRecPenView(LoginRequiredMixin,SuccessMessageMixin,JSONResponseMixin, View):
  template_name = 'home.html'
  output_template = get_template('home.html')

  def get(self, request, *args, **kwargs):
      
        try:
                #obj = self.get_object()
                tipos = Reclamo.objects.filter(std_rec__act_calculo=True).values('id_tipo_rec__dsc_tipo_rec').annotate(cant=Count('id_tipo_rec')).order_by('id_tipo_rec')
                label = []
                data = []
                for to in tipos:
                    
                    label.append(to['id_tipo_rec__dsc_tipo_rec'])
                    data.append(to['cant'])
                
                x = list(zip(label, data))

                x.sort(key=lambda x: x[1], reverse=True)
                x = list(zip(*x))
                
                #return JsonResponse({'labels': x[0][:3], 'data': x[1][:3]})
                
                return self.render_to_json_response({'labels': x[0][:3], 'data': x[1][:3]})

        except Exception as e:
             print('entro en la exeption***********')
             print(e)
             mensaje='No se ha podido editar el Registro'
             error="e"
             response=JsonResponse({'mensaje':mensaje, 'error':error})
             response.status_code=400
             return response
 
 



class FiltrosPagosView(LoginRequiredMixin,SuccessMessageMixin,JSONResponseMixin, View):
    template_name = 'home.html'
    output_template = get_template('home.html')

    def get(self, request, *args, **kwargs):
        
            try:    
                
                
                    #pago=tipos = Reclamo.objects.filter(std_rec__dsc_std__iexact="RECLAMO PAGADO", year_credito__gt=0).values('id_rec').annotate(min_year=Min('year_credito'))[:1].get()
                    pago= Reclamo.objects.filter(std_rec__dsc_std__iexact="RECLAMO PAGADO", year_credito__gt=0).values('year_credito').annotate(cant=Count('year_credito'))
                    
                    label = []
                    data = []
                    
                    
                    for f in pago:
                        label.append(f['year_credito'])
                        data.append(f['cant'])
                    
                    
                    x = list(zip(label, data))

                    x.sort(key=lambda x: x[1], reverse=True)
                    x = list(zip(*x))
                    
                                
                    return self.render_to_json_response({'labels': x[0][:], 'data': x[1][:]})
                    
                    
                    
                    
                
            except Exception as e:
             print('entro en la exeption***********')
             print(e)
             mensaje='No se ha podido editar el Registro'
             error="e"
             response=JsonResponse({'mensaje':mensaje, 'error':error})
             response.status_code=400
             return response    
 



class FiltrosPendView(LoginRequiredMixin,SuccessMessageMixin,JSONResponseMixin, View):
    template_name = 'home.html'
    output_template = get_template('home.html')

    def get(self, request, *args, **kwargs):
        
            try:         
                
                    pago= Reclamo.objects.all().values('fch_dsd_rec__year').annotate(cant=Count('fch_dsd_rec__year', distinct=True))
                    mo=[]
                    
                    for mos in pago:
                        
                        movim={
                            'year':mos['fch_dsd_rec__year'],
                            'cant': mos['cant'],
                        }
                        mo.append(movim)
                
                            
                    return self.render_to_json_response({'movs':mo})
                
            except Exception as e:
             print('entro en la exeption***********')
             print(e)
             mensaje='No se ha podido editar el Registro'
             error="e"
             response=JsonResponse({'mensaje':mensaje, 'error':error})
             response.status_code=400
             return response    
 



class FiltroTipoPagoView(LoginRequiredMixin,SuccessMessageMixin,JSONResponseMixin, View):
  template_name = 'home.html'
  output_template = get_template('home.html')

  def get(self, request, *args, **kwargs):
    
        try:
    
                filtros=(request.GET.get('param',None))
                
                
                filt=[int(valor) for valor in filtros.split(',')if valor]
            
                
                
                
               
                pago= Reclamo.objects.filter(std_rec__dsc_std__iexact="RECLAMO PAGADO", year_credito__in=filt).values('year_credito').annotate(cant=Count('year_credito'))
                
                
                
            
                
                label = []
                data = []
                
                    
                for to in pago:
                    
                    label.append(to['year_credito'])
                    data.append(to['cant'])
                    

                x = list(zip(label, data))
                
                x.sort(key=lambda x: x[1], reverse=True)
                x = list(zip(*x))
                
                print('---------------------------------')
                
                print( x[0][:])
                print( x[1][:])
                
                
                print('---------------------------------')
            
                #return JsonResponse({'labels': x[0][:3], 'data': x[1][:3]})
                #el label y el data no los ocupo
            
                return self.render_to_json_response({'labels': x[0][:], 'data': x[1][:]})
                
    
        except Exception as e:
             print('entro en la exeption***********')
             print(e)
             mensaje='No se ha podido editar el Registro'
             error="e"
             response=JsonResponse({'mensaje':mensaje, 'error':error})
             response.status_code=400
             return response
   

class FiltroTipoPendView(LoginRequiredMixin,SuccessMessageMixin,JSONResponseMixin, View):
  template_name = 'home.html'
  output_template = get_template('home.html')

  def get(self, request, *args, **kwargs):
    
        try:
    
                filtros=(request.GET.get('param',None))
                
                
                filt=[int(valor) for valor in filtros.split(',')if valor]
            
                pago= Reclamo.objects.filter(fch_dsd_rec__year__in=filt).values('fch_dsd_rec__year').annotate(cant=Count('fch_dsd_rec__year'))               
                
                
                
                label = []
                data = []
                
                    
                for to in pago:
                    
                    label.append(to['fch_dsd_rec__year'])
                    data.append(to['cant'])
                    
                             
                x = list(zip(label, data))
                
                x.sort(key=lambda x: x[0], reverse=True)
                x = list(zip(*x))
                
                
            
                return self.render_to_json_response({'labels': x[0][:], 'data': x[1][:]})
                
    
        except Exception as e:
             print('entro en la exeption***********')
             print(e)
             mensaje='No se ha podido editar el Registro'
             error="e"
             response=JsonResponse({'mensaje':mensaje, 'error':error})
             response.status_code=400
             return response
   
class EstadoYearCantView(LoginRequiredMixin,SuccessMessageMixin,JSONResponseMixin, View):
  template_name = 'home.html'
  output_template = get_template('home.html')

  def get(self, request, *args, **kwargs):
      
        try:
                
                #obj = self.get_object()
                movs = Estado.objects.all()
                series=[]
                label = []
                data = []
                datacant=[]
                datayear=[]
                year_data=set()
                leyenda=set()
                filt=[]
                
                year_actual=date.today().year+1
                year_min=Reclamo.objects.all().aggregate(minimo=Min('fch_dsd_rec__year'))
                
                for i in range(year_min['minimo'],year_actual):
                    filt.append(i)
                    
                
                #rec = Reclamo.objects.all().values('fch_dsd_rec__year','std_rec__dsc_std').annotate(cant=Count('fch_dsd_rec__year'), cantstd=Count('std_rec__dsc_std'))
                
                
               
                for mov in movs:    
                    leyenda.add((mov.dsc_std).title())
                    
                    datayear.clear()
                    serie={} 
                    
                    
                    for year in filt:
                        year_data.add(year)
                        
                        
                        
                        
                        datos= Reclamo.objects.filter(fch_dsd_rec__year=year, std_rec__dsc_std__iexact=mov.dsc_std)
                        
                        
                        datayear.append(datos.count())
                        
                    data=datayear[:]    
                   
                   
                        
                                         
                    serie={
                            'name': (mov.dsc_std).title(),
                            
                            'data': data
                        }
                    
                        
                    series.append(serie) 
   

                
                datosx=list(year_data)
               
                leyendax=list(leyenda)
               
                return self.render_to_json_response({'labels': leyendax, 'data': datosx, 'cant': series})
            
        except Exception as e:
             print('entro en la exeption***********')
             print(e)
             mensaje='No se ha podido editar el Registro'
             error="e"
             response=JsonResponse({'mensaje':mensaje, 'error':error})
             response.status_code=400
             return response

