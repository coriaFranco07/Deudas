from django.urls import path
from .views import ListMovData, EditMovData, AddMovData, DeleteMovData, Recuperar, Adquirir, Inventariar, Transferir

urlpatterns = [
    path('', ListMovData.as_view(), name='list_movdatas'),
    path('edit_movdata/<slug>', EditMovData.as_view(), name='edit_movdata'),
    path('add_movdata',AddMovData.as_view(), name='add_movdata' ),
    path('del_movdata/<slug>',DeleteMovData.as_view(), name='del_movdata' ),
    path('transf_movdata/<slug>',Recuperar.as_view(), name='recuperar' ),
    path('adquiere_movdata/<slug>',Adquirir.as_view(), name='adquirir' ),
    path('inventariar_bien/<slug>',Inventariar.as_view(), name='inventariar' ),
    path('transferir_bien/<slug>',Transferir.as_view(), name='transferir' ),
     
]
