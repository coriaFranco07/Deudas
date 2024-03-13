from apps.reclamo.models import Reclamo
from apps.prioridad.models import Prioridad
from apps.rec_prioridad.models import Rec_Prioridad

class Orden:
    
    def recalc_prior (self, user, hoy):
        
        
        rec=Reclamo.objects.filter(std_rec__act_calculo = True)
        prior=self.return_rec_prior()
        nro_orden=1
        for com in prior:
            mod_prior= Rec_Prioridad.objects.update()
            updateprior=Rec_Prioridad.objects.filter(slug=com.slug).update(orden=nro_orden, user_rec_prior=user, fch_orden=hoy)
            nro_orden +=1
        
        return
    
    
    
    
    def return_rec_prior (self):
        prior = Rec_Prioridad.objects.filter(id_rec__std_rec__act_calculo=True).order_by('-id_prior__nivel_prior','id_mov__fch_std_mov')
        return prior