from django.urls import path
from .views import ListTipo, EditTipo, AddTipo, DeleteTipo


urlpatterns = [
    path('', ListTipo.as_view(), name='list_tipos'),
    path('edit_tipo/<slug>', EditTipo.as_view(), name='edit_tipo'),
    path('add_tipo',AddTipo.as_view(), name='add_tipo' ),
    path('del_tipo/<slug>',DeleteTipo.as_view(), name='del_tipo' )
    
    
]
