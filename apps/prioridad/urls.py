from django.urls import path
from .views import ListPrioridad, AddPrioridad, EditPrioridad, DeletePrioridad


urlpatterns = [
    path(' ', ListPrioridad.as_view(), name='list_prioridades'),
    path('edit_prioridad/<slug>', EditPrioridad.as_view(), name='edit_prioridad'),
    path('add_prioridad',AddPrioridad.as_view(), name='add_prioridad' ),
    path('del_prioridad/<slug>',DeletePrioridad.as_view(), name='del_prioridad' )
    
    
]
