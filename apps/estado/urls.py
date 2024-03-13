from django.urls import path
from .views import ListEstado, EditEstado, DeleteEstado, AddEstado


urlpatterns = [
    path('', ListEstado.as_view(), name='list_estado_rec'),
    path('edit_estado_reclamo/<slug>', EditEstado.as_view(), name='edit_estado_rec'),
    path('add_estado_reclamo ',AddEstado.as_view(), name='add_estado_rec' ),
    path('del_estado_reclamo/<slug>',DeleteEstado.as_view(), name='del_estado_rec' )
    
    
]
