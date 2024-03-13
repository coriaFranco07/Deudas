from django.urls import path
from .views import ListModelo, EditModelo, AddModelo, DeleteModelo


urlpatterns = [
    path('', ListModelo.as_view(), name='list_modelos'),
    path('edit_modelo/<slug>', EditModelo.as_view(), name='edit_modelo'),
    path('add_modelo',AddModelo.as_view(), name='add_modelo' ),
    path('del_modelo/<slug>',DeleteModelo.as_view(), name='del_modelo' )
    
    
]