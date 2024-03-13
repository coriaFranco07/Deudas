from django.urls import path
from .views import ListEstMov,EditEstMov, AddEstMov,DeleteEstMov


urlpatterns = [
    path('', ListEstMov.as_view(), name='list_estados'),
    path('edit_estado<slug>', EditEstMov.as_view(), name='edit_estado'),
    path('add_estado',AddEstMov.as_view(), name='add_estado' ),
    path('del_estado/<slug>',DeleteEstMov.as_view(), name='del_estado' )
    
    
]
