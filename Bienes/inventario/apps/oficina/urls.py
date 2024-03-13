from django.urls import path
from .views import ListOficina, EditOficina, AddOficina, DeleteOficina


urlpatterns = [
    path('', ListOficina.as_view(), name='list_oficinas'),
    path('edit_oficina/<slug>', EditOficina.as_view(), name='edit_oficina'),
    path('add_oficina',AddOficina.as_view(), name='add_oficina' ),
    path('del_oficina/<slug>',DeleteOficina.as_view(), name='del_oficina' )
 
]
