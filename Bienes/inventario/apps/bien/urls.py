from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ListBien, EditBien, AddBien, DeleteBien

urlpatterns = [
    path('', ListBien.as_view(), name='list_bienes'),
    path('edit_bien/<slug>', EditBien.as_view(), name='edit_bien'),
    path('add_bien',AddBien.as_view(), name='add_bien' ),
    path('del_bien/<slug>',DeleteBien.as_view(), name='del_bien' ),
    
    
    
    
] 
