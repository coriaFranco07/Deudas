from django.urls import path
from .views import ListLegajo, EditLegajo, DeleteLegajo, AddLegajo


urlpatterns = [
    path('', ListLegajo.as_view(), name='list_legajos'),
    path('edit_legajo/<slug>', EditLegajo.as_view(), name='edit_legajo'),
    path('add_legajo ',AddLegajo.as_view(), name='add_legajo' ),
    path('del_legajo/<slug>',DeleteLegajo.as_view(), name='del_legajo' )
    
    
]
