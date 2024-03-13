from django.urls import path
from .views import ListTipoeRec, EditTipoRec,DeleteTipoRec,AddTipoRec

urlpatterns = [
    path('', ListTipoeRec.as_view(), name='list_tipos_rec'),
    path('edit_tipo_rec/<slug>', EditTipoRec.as_view(), name='edit_tipo_rec'),
    path('add_lote',AddTipoRec.as_view(), name='add_tipo_rec' ),
    path('del_lote/<slug>',DeleteTipoRec.as_view(), name='del_tipo_rec' )
    
    
]
