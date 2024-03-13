from django.urls import path
from .views import home, TiposRecView, RecPeriodosView,RecPedienteView,RecPagadoView,PresupuestoView,RecLoteiew,CantTipoRecView,TipoMovView,ReclamosPendView,FiltroTipoMovView, FiltrosMovView, TiposRecViewTres, CantTipoRecPenView, FiltrosPagosView, FiltrosPendView, FiltroTipoPagoView, FiltroTipoPendView, EstadoYearCantView
urlpatterns = [
    
    path('', home, name='home'),
    path('total_rec_pendientes', RecPedienteView.as_view(), name='total_rec_pendientes'),
    path('total_rec_pagados', RecPagadoView.as_view(), name='total_rec_pagados'),
    path('reclamos_periodos', RecPeriodosView.as_view(), name='reclamos_periodos'),
    #path('tipos_reclamos', TiposRecView.as_view(), name='tipos_reclamos'),
    path('tipos_reclamos', TiposRecViewTres.as_view(), name='tipos_reclamos'),
    path('presupuesto', PresupuestoView.as_view(), name='presupuesto'),
    path('reclamosenlotes', RecLoteiew.as_view(), name='reclamosenlotes'),
    path('cantportipo', CantTipoRecView.as_view(), name='cantportipo'),
    path('cantportipopen', CantTipoRecPenView.as_view(), name='cantportipopen'),
    
    path('tipomov', TipoMovView.as_view(), name='tipomov'),
#    path('grafico_select', filtros, name='grafico_select'),

     path('grafico_select', FiltroTipoMovView.as_view(), name='grafico_select'),
     path('filtros_mov', FiltrosMovView.as_view(), name='filtros_mov'),
     
     
     path('reclamos_pendientes', ReclamosPendView.as_view(), name='reclamos_pendientes'),
     path('filtros_pagos', FiltrosPagosView.as_view(), name='filtros_pagos'),
     path('filtros_pend', FiltrosPendView.as_view(), name='filtros_pend'),
     
     path('grafico_pagos', FiltroTipoPagoView.as_view(), name='grafico_pagos'),
     path('grafico_pend', FiltroTipoPendView.as_view(), name='grafico_pend'),
     
     path('EstadoYearCantView', EstadoYearCantView.as_view(), name='EstadoYearCantView'),
    
    
]
