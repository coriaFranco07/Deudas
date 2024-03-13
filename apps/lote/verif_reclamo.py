
from apps.lote.models import Lote
from apps.rec_lote.models import Rec_Lote
from apps.estado.models import  Estado
from datetime import date
from django.db.models import Max
from apps.deuda.models import Deuda
from apps.reclamo.models import Reclamo


class Verif_Lotes:
    
    def rec_in_lote(self,slug):
        
        rec=Rec_Lote.objects.filter(id_rec__slug=slug, id_lote__activo_lote=False)
        if rec:
           
            return True
        
        
        return False
    

    def unico_lote(self, slug, estado, usuario):
        
        
        val_estado=Estado.objects.get(pk=estado)
        
        if val_estado.dsc_std.upper()=='RECLAMO PAGADO':
            print('reclamo pagado')
            if not self.rec_in_lote(slug):
                print('antes del year_lote')
                year_lote = date.today().year
                print(year_lote)
                lote=Lote.objects.filter(year_lote=year_lote).aggregate(Max('nivel_lote'))
                print('antes del if')
                
                if lote['nivel_lote__max']:
                    print('nivel=++++++')
                    nivel=int(lote['nivel_lote__max'])+1
                else:
                    print('nivel=1')
                    
                    nivel=1
                    
                print('nivelllllllll')
                print(nivel)    
                deuda=Deuda.objects.get(id_rec__slug=slug)
                
                new_lote=Lote.objects.create(
                    nivel_lote=nivel,
                    year_lote=year_lote,
                    activo_lote=False,
                    importe_lote=deuda.total,
                    saldo_lote=0,
                    user_lote=usuario,
                )    
                
                print('ahora el reclamo al lote')
                new_rec=Rec_Lote.objects.create(
                    id_lote=new_lote,
                    id_rec=deuda.id_rec,
                    user_rec_lote=usuario,
                )  
                
                print('datos reclamo en lote')
                print(new_rec)
                
                
            return False
        return True
    
    
    def supl_rec(self, slug, estado):
        
        valor = False
        est=Estado.objects.get(pk=estado)
        if est.dsc_std.upper() == "RECLAMO PAGADO":
                supl=Reclamo.objects.get(slug=slug)
                    
                if not supl.nro_supl or not supl.year_credito:
                    
                    valor=True
        
        return valor        

    
    
    def deuda_rec(self, slug, estado):
        valor = True
        
        val_estado=Estado.objects.get(pk=estado)
        deuda=Deuda.objects.get(id_rec__slug=slug)
        if val_estado.dsc_std.upper()=='RECLAMO PAGADO' and deuda.total ==0:
            valor=False
        
        return valor