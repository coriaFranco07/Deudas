
from apps.lote.models import Lote
from apps.rec_prioridad.models import Rec_Prioridad
from apps.deuda.models import Deuda
from apps.rec_lote.models import Rec_Lote
from django.contrib.auth.models import User
from apps.estado.models import Estado
from django.utils import timezone
from apps.reclamo.models import Reclamo


class Pago_Lote:
    
    def pagar_lote(self,slug,user):
        print('******************************************************+++')
        usuario=User.objects.get(username=user)
        recl=Rec_Lote.objects.filter(id_lote__slug=slug)
        
        instance_std, created_std=Estado.objects.get_or_create(dsc_std='RECLAMO PAGADO', defaults={'user_std':usuario, 'act_calculo':False})
        
        print(f'instance: {instance_std} - created {created_std}')
        print(type(instance_std))
        # lotes=Lote.objects.filter(activo_lote=True).order_by('year_lote','nivel_lote')
        # recl=Rec_Prioridad.objects.filter(orden__gte=0,id_rec__std_rec__act_calculo=True).order_by('orden')
        # Rec_Lote.objects.all().delete()
        # lotes_inc=[]
        rec_inc=[]
        supl=True
        # print('----------------------1-------------------------')
        for rec in recl:
            rec.id_rec.std_rec=instance_std
            rec.id_rec.user_rec=usuario
            rec.id_rec.fch_rec=timezone.datetime.today()
            if not rec.id_rec.year_credito or not rec.id_rec.nro_supl:
                supl=False
                break
            else:
                
                rec_inc.append(rec.id_rec)
        
        if supl:
                Reclamo.objects.bulk_update(rec_inc,['std_rec','user_rec','fch_rec'])
                Lote.objects.filter(slug=slug).update(activo_lote=False, user_lote=usuario, fch_lote=timezone.datetime.today())
                #             lotes_inc.clear()
                #             print(f'saldo enviado: {saldo}')
                #         elif val==0:
                #             break
                        
            
        #     Lote.objects.filter(slug=lo.slug).update(saldo_lote=saldo, user_lote=usuario)
                
                 
        return supl
        
    
         