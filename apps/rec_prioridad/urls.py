from django.urls import path
from .views import EditPrioridad


urlpatterns = [
    
    path('edit_rec_prior/<slug>/<str:slug_mov>', EditPrioridad.as_view(), name='edit_rec_prior'),
    
    
    
]
