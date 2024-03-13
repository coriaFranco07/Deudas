from django.urls import path
from .views import ListEstado, EditEstado, AddEstado, DeleteEstado


urlpatterns = [
    path('', ListEstado.as_view(), name='list_estados'),
    path('edit_estado/<slug>', EditEstado.as_view(), name='edit_estado'),
    path('add_estado',AddEstado.as_view(), name='add_estado' ),
    path('del_estado/<slug>',DeleteEstado.as_view(), name='del_estado' )
    
    
]
