from django.urls import path, include
from .views import ListReclamos, EditReclamo, AddReclamo, DeleteReclamo, index, EditSuple
urlpatterns = [
    path('', ListReclamos.as_view(), name='list_reclamos'),
    path('edit_reclamo/<slug>', EditReclamo.as_view(), name='edit_reclamo'),
    path('add_reclamo',AddReclamo.as_view(), name='add_reclamo' ),
    path('del_reclamo/<slug>',DeleteReclamo.as_view(), name='del_reclamo' ),
    path('edit_supl_rec/<slug>',EditSuple.as_view(), name='edit_supl_rec' ),
    
    
    
]
