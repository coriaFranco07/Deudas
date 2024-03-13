from django.urls import path
from .views import EditDeuda


urlpatterns = [
    
    path('edit_rec_deuda/<slug>', EditDeuda.as_view(), name='edit_rec_deuda'),
    
    
    
]
