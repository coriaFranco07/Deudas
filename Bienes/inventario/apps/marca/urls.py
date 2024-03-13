from django.urls import path
from .views import ListMarca, EditMarca, AddMarca, DeleteMarca


urlpatterns = [
    path('', ListMarca.as_view(), name='list_marcas'),
    path('edit_marca/<slug>', EditMarca.as_view(), name='edit_marca'),
    path('add_marca',AddMarca.as_view(), name='add_marca' ),
    path('del_marca/<slug>',DeleteMarca.as_view(), name='del_marca' )
    
    
]
