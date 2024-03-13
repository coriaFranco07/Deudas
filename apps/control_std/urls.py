from django.urls import path
from .views import ListControlEstado, EditControlEstado, AddControlEstado, DeleteControlEstado


urlpatterns = [
    path('', ListControlEstado.as_view(), name='list_controles_std'),
    path('edit_control_std/<slug>', EditControlEstado.as_view(), name='edit_control_std'),
    path('add_control_std ',AddControlEstado.as_view(), name='add_control_std' ),
    path('del_control_std/<slug>',DeleteControlEstado.as_view(), name='del_control_std' )
    
    
]
