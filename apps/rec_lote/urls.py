from django.urls import path
from .views import ListReclamosLotes
urlpatterns = [
    
    path('reclamos_lotes_list/<slug>',ListReclamosLotes.as_view(), name='reclamos_lotes_list' ),
   
    
    
]
