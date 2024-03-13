from django.urls import path
from .views import ListClase, EditClase, AddClase, DeleteClase


urlpatterns = [
    path('', ListClase.as_view(), name='list_clases'),
    path('edit_clase/<slug>', EditClase.as_view(), name='edit_clase'),
    path('add_clase',AddClase.as_view(), name='add_clase' ),
    path('del_clase/<slug>',DeleteClase.as_view(), name='del_clase' )
    
    
]