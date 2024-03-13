from django.urls import path
from .views import Listlote, EditLote, AddLote, DeleteLote, ListloteAcivo, calcular_lotes, pagar_lote

urlpatterns = [
    path('', Listlote.as_view(), name='list_lotes'),
    path('lotes_activos', ListloteAcivo.as_view(), name='list_lotes_a'),
    path('edit_lote/<slug>', EditLote.as_view(), name='edit_lote'),
    path('add_lote',AddLote.as_view(), name='add_lote' ),
    path('del_lote/<slug>',DeleteLote.as_view(), name='del_lote' ),
    path('calcular_lotes/<user>/<int:val>',calcular_lotes, name='calcular_lotes' ),
    path('generar_pago/<slug>/<user>',pagar_lote, name='generar_pago' ),
    
    
]
