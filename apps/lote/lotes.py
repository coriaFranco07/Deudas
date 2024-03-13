
from apps.lote.models import Lote
from apps.rec_prioridad.models import Rec_Prioridad
from apps.deuda.models import Deuda
from apps.rec_lote.models import Rec_Lote
from django.contrib.auth.models import User

class Calc_Lotes:
    
    def rec_lote(self,user,val):
        usuario=User.objects.get(username=user)
        
        lotes=Lote.objects.filter(activo_lote=True).order_by('year_lote','nivel_lote')
        recl=Rec_Prioridad.objects.filter(orden__gt=0,id_rec__std_rec__act_calculo=True, id_rec__deudas_reclamos__total__gt=0).order_by('orden')
       
        borrados=Rec_Lote.objects.filter(id_lote__activo_lote=True).delete()
        
        lotes_inc=[]
        rec_inc=[]
        print('----------------------1-------------------------')
        for lo in lotes:
            valor=lo.importe_lote
            saldo=valor
            print(f'valor lote {valor}  saldo: {saldo}')
            print('----------------------2-------------------------')
            for re in recl:
                   
                            print(re)
                            deuda = Deuda.objects.get(id_rec__slug=re.id_rec.slug)
                            if deuda.total <= saldo:
                                
                                data=Rec_Lote(
                                    id_lote=lo,
                                    id_rec=re.id_rec,
                                    user_rec_lote=usuario,
                                    
                                )
                                print('----------------------3-------------------------')
                                if re in rec_inc:
                                    pass
                                else:
                                    saldo -= deuda.total
                                    lotes_inc.append(data)
                                    rec_inc.append(re)
                                Rec_Lote.objects.bulk_create(lotes_inc)
                                lotes_inc.clear()
                                print(f'saldo enviado: {saldo}')
                            elif val==0:
                                break
                        
            
            Lote.objects.filter(slug=lo.slug).update(saldo_lote=saldo, user_lote=usuario)
                
                 
        print('calculando el lote')
        
    
         