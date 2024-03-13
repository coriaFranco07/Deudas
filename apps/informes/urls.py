from django.urls import path
from .views import InformesView, InformesGDEView

urlpatterns = [
    path('informes',InformesView.as_view(), name='informes'),
    path('movs_info',InformesGDEView.as_view(), name='movs_info'),   
    
]
