from django.urls import path
from .views import ListMovimientos, AddMovimiento, EditMovRec, DeleteMovRec
urlpatterns = [
    path('<slug>', ListMovimientos.as_view(), name='list_detalles'),
    path('edit_mov_rec/<slug>', EditMovRec.as_view(), name='edit_mov_rec'),
    path('add_mov_rec/<slug>',AddMovimiento.as_view(), name='add_mov_rec' ),
    path('del_mov_rec/<slug>',DeleteMovRec.as_view(), name='del_mov_rec' )
    
    
]
