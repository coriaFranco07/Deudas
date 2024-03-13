from django.urls import path
from .views import ListAdmin,AddAdmin,EditAdmin,DeleteAdmin, reset_axe, ListAdminHistorial


urlpatterns = [
    path('', ListAdmin.as_view(), name='list_admins'),
    path('add_admin',AddAdmin.as_view(), name='add_admin' ),
    path('edit_admin/<int:user_id>/', EditAdmin.as_view(), name='edit_admin'),
    path('del_admin/<int:pk>/', DeleteAdmin.as_view(), name='del_admin'),
    path('reset_user/<int:pk>/', reset_axe.as_view(), name='reset_user'),
    path('adminHist', ListAdminHistorial.as_view(), name='adminHist'),
    
    
]
