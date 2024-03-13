from django.urls import path
from .views import ListOperador, EditOperador, AddOperador, DeleteOperador


urlpatterns = [
    path('', ListOperador.as_view(), name='list_operadores'),
    path('edit_oper/<slug>', EditOperador.as_view(), name='edit_operador'),
    path('add_oper',AddOperador.as_view(), name='add_operador' ),
    path('del_oper/<slug>',DeleteOperador.as_view(), name='del_operador' )
    
    
]
